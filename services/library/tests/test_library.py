from __future__ import annotations
import asyncio
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from mcp import Client
from mcp.client.stdio import StdioServerParameters

from prim_library.library import Library, LibraryError, fingerprint, load_json, check_schema, version_key, scores
from prim_library.cli import create
from prim_library.server import create_server
from prim_library.popularity import Signals, sign

RESEARCH = 'primfoundation/research'
RV = '0.3.0-dev.3'


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.library = Library()

    def test_profiles_no_repository_requirement(self):
        ids = {row['id'] for row in self.library.search()['items']}
        self.assertEqual(ids, {RESEARCH, 'primfoundation/person', 'primfoundation/decision', 'primfoundation/workbook', 'primfoundation/coding-agent-harness'})
        for row in self.library.search()['items']:
            self.assertTrue(row['creation_available'])
            self.assertNotIn('repo', self.library.get(row['id'])['metadata'])

    def test_search_relevance_and_empty_result(self):
        self.assertEqual(self.library.search('research')['items'][0]['id'], RESEARCH)
        self.assertEqual(self.library.search('nonexistent abbreviation')['items'], [])

    def test_pagination_and_filters(self):
        first = self.library.search(limit=1)
        second = self.library.search(limit=1, offset=first['next_offset'])
        self.assertNotEqual(first['items'][0]['id'], second['items'][0]['id'])
        self.assertEqual(self.library.search(maturity='stable')['total'], 0)

    def test_no_popularity_is_not_fabricated(self):
        rows = self.library.search(sort='popular')['items']
        self.assertEqual([r['id'] for r in rows], sorted(r['id'] for r in rows))
        for row in rows:
            self.assertEqual(row['popularity']['status'], 'no_data')
            self.assertEqual(row['popularity']['popular_score'], 0)

    def test_invalid_search_bounds(self):
        for kwargs in [{'limit':0},{'limit':100},{'limit':True},{'offset':-1},{'query':'x'*257},{'sort':'advertising'}]:
            with self.subTest(kwargs=kwargs),self.assertRaises(LibraryError): self.library.search(**kwargs)

    def test_exact_version_and_digest(self):
        x=self.library.get(RESEARCH, RV)
        self.assertEqual(x,self.library.get(RESEARCH,RV,x['definition_sha256']))
        with self.assertRaises(LibraryError):self.library.get(RESEARCH,RV,'0'*64)
        with self.assertRaises(LibraryError):self.library.get(RESEARCH,'7.0.0')
        with self.assertRaises(LibraryError):self.library.get('research')

    def test_semver_order_and_invalid_versions(self):
        self.assertLess(version_key('1.0.0-dev.2'),version_key('1.0.0-dev.10'))
        self.assertLess(version_key('1.0.0-rc.1'),version_key('1.0.0'))
        self.assertLess(version_key('1.0.0-2'),version_key('1.0.0-alpha'))
        self.assertEqual(version_key('1.0.0+build1'),version_key('1.0.0+build2'))
        for bad in ['1','v1.0.0','01.0.0','1.0.0-dev.01']:
            with self.subTest(bad=bad),self.assertRaises(LibraryError):version_key(bad)

    def test_resource_progressive_loading_and_no_traversal(self):
        a=self.library.resource(RESEARCH,RV,'manifest',limit=20)
        b=self.library.resource(RESEARCH,RV,'manifest',offset=a['next_offset'],limit=20)
        full=self.library.get(RESEARCH,RV)['resources']['manifest']['text']
        self.assertEqual(a['text']+b['text'],full[:40])
        for name in ['../LICENSE','/etc/passwd','https://example.com','compatibility/orf/validate.py']:
            with self.subTest(name=name),self.assertRaises(LibraryError):self.library.resource(RESEARCH,RV,name)

    def test_complete_definition_hash_covers_schema_not_just_manifest(self):
        entry=self.library.get(RESEARCH,RV)
        old=entry['definition_sha256']
        entry['resources']['schema']['text']+=' '
        self.assertNotEqual(old,fingerprint({'metadata':entry['metadata'],'resources':entry['resources']}))

    def test_definition_mutation_does_not_change_server(self):
        x=self.library.get(RESEARCH,RV); x['metadata']['name']='changed'
        self.assertNotEqual(self.library.get(RESEARCH,RV)['metadata']['name'],'changed')

    def test_snapshot_tampering_rejected(self):
        s=deepcopy(self.library._snapshot);s['definitions'][0]['metadata']['name']='forged'
        with self.assertRaises(LibraryError):Library(s)
        s['snapshot_sha256']=fingerprint(s['definitions'])
        with self.assertRaises(LibraryError):Library(s)

    def test_remote_refs_and_regex_schemas_rejected(self):
        for s in [{'$ref':'https://example.test/a'}, {'$ref':'file:///etc/passwd'}, {'type':'string','pattern':'(a+)+'}]:
            with self.subTest(schema=s),self.assertRaises(LibraryError):check_schema(s)

    def test_json_duplicate_keys_nonfinite_depth_and_size(self):
        for raw in [b'{"a":1,"a":2}',b'{"a":NaN}',b'['*30+b'0'+b']'*30,b'"'+b'x'*600000+b'"']:
            with self.assertRaises(LibraryError):load_json(raw)

    def record(self):
        result=self.library.kit(RESEARCH,RV)['template'];result['id']='test-investigation';return result

    def test_native_draft_valid_but_no_fact_or_approval_claim(self):
        r=self.library.validate(RESEARCH,RV,self.record())
        self.assertEqual(r['status'],'passed')
        self.assertEqual(r['checks']['human_review'],'not_verified')
        self.assertEqual(r['checks']['factual_accuracy'],'not_checked')

    def test_active_and_complete_require_real_question(self):
        for state in ['active','complete']:
            r=self.record();r['workflow_state']=state
            self.assertEqual(self.library.validate(RESEARCH,RV,r)['status'],'failed')

    def test_completed_inconclusive_result_is_valid(self):
        r=self.record();r.update(question='What is known?',workflow_state='complete',outcome='inconclusive')
        self.assertEqual(self.library.validate(RESEARCH,RV,r)['status'],'passed')

    def test_supported_claim_requires_declared_support_but_does_not_certify_it(self):
        r=self.record();r['claims']=[{'id':'c','text':'A claim','basis':'inference','support_state':'supported'}]
        self.assertEqual(self.library.validate(RESEARCH,RV,r)['status'],'failed')
        r['sources']=[{'id':'s','locator':'urn:example:source','kind':'artifact'}]
        r['evidence']=[{'id':'e','claim_id':'c','source_id':'s','relation':'supports'}]
        result=self.library.validate(RESEARCH,RV,r)
        self.assertEqual(result['status'],'passed');self.assertEqual(result['checks']['source_independence'],'not_checked')

    def test_dangling_reference_and_duplicate_ids(self):
        r=self.record();r['sources']=[{'id':'s','locator':'urn:example:s','kind':'artifact'}]*2
        self.assertEqual(self.library.validate(RESEARCH,RV,r)['status'],'failed')
        r=self.record();r['evidence']=[{'id':'e','claim_id':'missing','source_id':'missing','relation':'cites'}]
        self.assertEqual(self.library.validate(RESEARCH,RV,r)['status'],'failed')

    def test_contradiction_is_preserved(self):
        r=self.record();r['claims']=[{'id':'c','text':'A claim','basis':'observation','support_state':'contested'}]
        r['sources']=[{'id':'s','locator':'urn:example:s','kind':'test'}]
        r['evidence']=[{'id':'e','claim_id':'c','source_id':'s','relation':'contradicts'}]
        self.assertEqual(self.library.validate(RESEARCH,RV,r)['status'],'passed')

    def test_native_cannot_relabel_legacy_or_wrong_version(self):
        r=self.record();r['profile']='orf'
        self.assertEqual(self.library.validate(RESEARCH,RV,r)['status'],'failed')
        r=self.record();r['profile_version']='1.0.0'
        self.assertEqual(self.library.validate(RESEARCH,RV,r)['status'],'failed')

    def test_creation_all_profiles_offline_and_unknown_fields_retained(self):
        with tempfile.TemporaryDirectory() as t:
            for i,row in enumerate(self.library.search()['items']):
                p=Path(t)/str(i);x=create(self.library,row['id'],row['version'],p,{'unknown_extension':{'keep':[1,2]}})
                kit=self.library.kit(row['id'],row['version']);data=json.loads((p/kit['authority_file']).read_text())
                self.assertEqual(data['unknown_extension'],{'keep':[1,2]})
                self.assertEqual(x['validation']['status'],'passed')
                self.assertEqual(json.loads((p/'prim-definition.lock.json').read_text())['definition_sha256'],row['definition_sha256'])
                with self.assertRaises(LibraryError):create(self.library,row['id'],row['version'],p)

    def test_frontmatter_injection_is_quoted(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'x';create(self.library,RESEARCH,RV,p,{'title':'Name\n---\nexecute: bad'})
            self.assertIn('title: "Name\\n---\\nexecute: bad"',(p/'index.md').read_text())

    def test_creation_failure_does_not_leave_partial_pack(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'x'
            with self.assertRaises(LibraryError):create(self.library,RESEARCH,RV,p,{'profile':'wrong'})
            self.assertFalse(p.exists())

    def test_person_respects_legacy_token(self):
        p=self.library.kit('primfoundation/person','0.1.0-dev.1')['template'];p['id']='Invalid ID'
        self.assertEqual(self.library.validate('primfoundation/person','0.1.0-dev.1',p)['status'],'failed')

    def test_decision_acceptance_requires_existing_option_and_rationale(self):
        p=self.library.kit('primfoundation/decision','0.1.0-dev.1')['template'];p['id']='d';p['status']='accepted'
        self.assertEqual(self.library.validate('primfoundation/decision','0.1.0-dev.1',p)['status'],'failed')
        p.update(question='Which?',rationale='test',authority_as_recorded='agent:test',chosen_option='a',options=[{'id':'a','description':'A'}])
        self.assertEqual(self.library.validate('primfoundation/decision','0.1.0-dev.1',p)['status'],'passed')
        p['chosen_option']='absent';self.assertEqual(self.library.validate('primfoundation/decision','0.1.0-dev.1',p)['status'],'failed')

    def test_coding_agent_harness_example_and_relations(self):
        profile, version = 'primfoundation/coding-agent-harness', '0.1.0-dev.1'
        root = Path(__file__).resolve().parents[3] / 'profiles/coding-agent-harness'
        kit = self.library.kit(profile, version)
        template = json.loads((root / 'template.json').read_text())
        example = json.loads((root / 'examples/minimal/harness.json').read_text())
        self.assertEqual(kit['template'], template)
        self.assertEqual(kit['authority_file'], 'harness.json')
        for record in [template, example]:
            result = self.library.validate(profile, version, record)
            self.assertEqual(result['status'], 'passed', result)
            self.assertEqual(result['checks']['factual_accuracy'], 'not_checked')
            self.assertEqual(result['checks']['human_review'], 'not_verified')
        mutations = [
            ('profile', 'other/harness'), ('profile_version', '1.0.0'),
            ('kind', 'tool-evaluation'), ('status', 'approved'),
        ]
        for field, value in mutations:
            with self.subTest(field=field):
                self.assertEqual(self.library.validate(profile, version, {**example, field:value})['status'], 'failed')
        for collection in ['capabilities', 'components', 'capability_links', 'evidence',
                           'evaluations', 'evaluation_evidence', 'observations',
                           'incidents', 'procedures', 'changes', 'verifications']:
            record = deepcopy(example)
            record[collection].append(deepcopy(record[collection][0]))
            with self.subTest(collection=collection):
                self.assertEqual(self.library.validate(profile, version, record)['status'], 'failed')
        for collection, field in [
            ('capability_links','component_id'), ('capability_links','capability_id'),
            ('evaluations','subject'), ('evaluations','evidence_id'),
            ('evaluation_evidence','evaluation_id'), ('evaluation_evidence','evidence_id'),
            ('observations','subject'), ('observations','evidence_id'),
            ('incidents','subject'), ('incidents','evidence_id'),
            ('changes','incident_id'), ('changes','procedure_id'), ('changes','evidence_id'),
            ('verifications','change_id'), ('verifications','evidence_id')]:
            record = deepcopy(example)
            record[collection][0][field] = 'missing'
            with self.subTest(reference=(collection,field)):
                self.assertEqual(self.library.validate(profile, version, record)['status'], 'failed')
        for value in [-1, 101, 1.5, '70', None]:
            record = deepcopy(example)
            record['evaluations'][0]['ratings']['confidence'] = value
            self.assertEqual(self.library.validate(profile, version, record)['status'], 'failed')
        self.assertEqual(self.library.validate(profile, version, {**template, 'status':'observed'})['status'], 'failed')

    def test_workbook_profile_is_generic_and_structural(self):
        profile = 'primfoundation/workbook'
        version = '0.1.0-dev.1'
        row = self.library.search('workbook')['items'][0]
        self.assertEqual(row['id'], profile)
        self.assertEqual(row['version'], version)
        self.assertEqual(set(self.library.get(profile, version)['metadata']['kinds']), {'workbook', 'worksheet', 'measure', 'metric'})
        record = self.library.kit(profile, version)['template']
        record['workbook_id'] = 'workbook:test:metrics'
        record['title'] = 'Metrics'
        record['worksheets'] = [
            {'n': 1, 'id': 'plan', 'role': 'expected', 'pack': 'worksheets/plan', 'title': 'Plan'},
            {'n': 2, 'id': 'actuals', 'role': 'actuals', 'pack': 'worksheets/actuals', 'title': 'Actuals'},
        ]
        self.assertEqual(self.library.validate(profile, version, record)['status'], 'passed')
        record['worksheets'][1]['id'] = 'plan'
        self.assertEqual(self.library.validate(profile, version, record)['status'], 'failed')

    def test_workbook_schema_does_not_weaken_no_regex_boundary(self):
        kit = self.library.kit('primfoundation/workbook', '0.1.0-dev.1')
        self.assertNotIn('pattern', json.dumps(kit['schema']))
        self.assertEqual(kit['authority_file'], 'workbook.json')


class PopularityTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'signals.sqlite'
        self.key=b'k'*32;self.store=Signals(self.path,{'trusted':self.key},b's'*32);self.addCleanup(self.store.close)
        self.now=datetime.now(timezone.utc)

    def event(self,subject='person-1',kind='adoption',suffix='1',days=1):
        e={'issuer':'trusted','subject':subject,'profile_id':RESEARCH,'kind':kind,'event_id':subject+kind+suffix,
           'occurred_at':(self.now-timedelta(days=days)).isoformat(),'consent':True}
        return {**e,'signature':sign(e,self.key)}

    def send(self,e):return self.store.ingest(e,{RESEARCH},self.now)

    def test_replay_and_distinct_adoption_cap(self):
        e=self.event();self.assertEqual(self.send(e),'accepted');self.assertEqual(self.send(e),'duplicate')
        for n in range(10):self.send(self.event(suffix=str(n)))
        self.assertEqual(self.store.db.execute('select count(*) from adoption').fetchone()[0],1)

    def test_bad_signature_unknown_issuer_and_no_consent(self):
        for changes in [{'signature':'x'},{'issuer':'rogue'},{'consent':False},{'profile_id':'other/unknown'}]:
            with self.subTest(changes=changes),self.assertRaises(LibraryError):self.send({**self.event(),**changes})

    def test_expired_and_future_signal_rejected(self):
        for days in [-1,10]:
            with self.assertRaises(LibraryError):self.send(self.event(days=days))

    def test_small_cohorts_suppressed(self):
        for i in range(4):self.send(self.event(str(i)))
        row=self.store.export({RESEARCH},self.now)['profiles'][RESEARCH]
        self.assertEqual(row['status'],'insufficient_data');self.assertEqual(row['adoptions_7d'],0)

    def test_popular_profiles_rise_without_irrelevant_search_results(self):
        for i in range(6):self.send(self.event(str(i)));self.send(self.event(str(i),kind='star'))
        ranking=self.store.export({RESEARCH},self.now)
        lib=Library(rankings=ranking)
        self.assertEqual(lib.search(sort='popular')['items'][0]['id'],RESEARCH)
        self.assertEqual(lib.search(sort='trending')['items'][0]['id'],RESEARCH)
        self.assertNotIn(RESEARCH,[r['id'] for r in lib.search('person',sort='popular')['items']])

    def test_unstar_and_forgetting_remove_subject(self):
        self.send(self.event(kind='star',days=2));self.send(self.event(kind='unstar',days=1))
        self.assertEqual(self.store.db.execute('select active from stars').fetchone()[0],0)
        self.send(self.event());self.store.forget('trusted','person-1')
        self.assertEqual(self.store.db.execute('select count(*) from adoption').fetchone()[0],0)
        self.assertEqual(self.store.db.execute('select count(*) from stars').fetchone()[0],0)

    def test_out_of_order_star_cannot_restore_newer_unstar(self):
        self.send(self.event(kind='unstar',days=1));self.send(self.event(kind='star',days=2))
        self.assertEqual(self.store.db.execute('select active from stars').fetchone()[0],0)

    def test_raw_subject_not_stored_and_no_instance_fields_allowed(self):
        self.send(self.event(subject='private-identity-secret'))
        self.assertNotIn(b'private-identity-secret',self.path.read_bytes())
        e=self.event();e['private_prim']={'balance':100}
        with self.assertRaises(LibraryError):self.send(e)

    def test_reads_are_not_votes(self):
        with self.assertRaises(LibraryError):self.send(self.event(kind='view'))

    def test_scores_monotonic_and_growth_capped(self):
        a=scores({'stars':10,'adoptions_30d':10});b=scores({'stars':100,'adoptions_30d':100})
        self.assertGreater(b[0],a[0])
        self.assertGreater(scores({'adoptions_7d':100,'adoptions_previous_7d':1})[1],scores({'adoptions_7d':100,'adoptions_previous_7d':100})[1])
        with self.assertRaises(LibraryError):scores({'stars':-1})


class MCPTests(unittest.IsolatedAsyncioTestCase):
    async def test_sdk_tools_resources_prompt_and_creation_kit(self):
        async with Client(create_server()) as c:
            tools=await c.list_tools()
            names={t.name for t in tools.tools}
            self.assertEqual(names,{'prim_search','prim_get_definition','prim_list_versions','prim_get_resource','prim_get_creation_kit','prim_rankings'})
            self.assertNotIn('validate_prim',names);self.assertNotIn('vote',names)
            result=await c.call_tool('prim_search',{'query':'research'})
            self.assertFalse(result.is_error)
            data=result.structured_content
            row=data['items'][0]
            kit=await c.call_tool('prim_get_creation_kit',{'profile_id':row['id'],'version':row['version'],'expected_sha256':row['definition_sha256']})
            self.assertFalse(kit.is_error);self.assertEqual(kit.structured_content['schema']['type'],'object')
            resources=await c.list_resources();self.assertTrue(resources.resources)
            resource=await c.read_resource('prim://library/catalog');self.assertTrue(resource.contents)
            prompt=await c.get_prompt('create_a_prim',{'profile_id':RESEARCH,'version':RV});self.assertTrue(prompt.messages)

    async def test_pin_mismatch_is_error_result(self):
        async with Client(create_server()) as c:
            result=await c.call_tool('prim_get_creation_kit',{'profile_id':RESEARCH,'version':RV,'expected_sha256':'bad'})
            self.assertTrue(result.is_error)

    async def test_stdio_real_process_with_modern_and_legacy_clients(self):
        for mode in ['auto','legacy']:
            params=StdioServerParameters(command=sys.executable,args=['-m','prim_library.server'],env={**os.environ})
            async with Client(params,mode=mode,read_timeout_seconds=15) as c:
                result=await c.call_tool('prim_search',{'query':'person'})
                self.assertFalse(result.is_error);self.assertEqual(result.structured_content['items'][0]['id'],'primfoundation/person')


class HTTPTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        import socket,time,urllib.request
        with socket.socket() as sock:
            sock.bind(('127.0.0.1',0));cls.port=sock.getsockname()[1]
        env={**os.environ,'PRIM_ALLOWED_HOSTS':f'127.0.0.1:{cls.port}','PRIM_ALLOWED_ORIGINS':''}
        cls.proc=subprocess.Popen([sys.executable,'-m','prim_library.server','--transport','http','--port',str(cls.port)],
                                  env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        cls.url=f'http://127.0.0.1:{cls.port}'
        for _ in range(100):
            if cls.proc.poll() is not None:
                raise AssertionError(cls.proc.communicate()[1].decode())
            try:
                with urllib.request.urlopen(cls.url+'/healthz',timeout=0.2) as r:
                    if r.status==200: return
            except OSError:time.sleep(0.05)
        cls.proc.terminate();cls.proc.wait();raise AssertionError('HTTP did not start')

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        try: cls.proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:cls.proc.kill();cls.proc.communicate()

    def test_public_web_api_discovery_and_definition(self):
        import urllib.request
        for path in ['/', '/api/prims?sort=popular', '/.well-known/prim-library.json',
                     '/api/definitions/primfoundation/research/0.3.0-dev.3']:
            with urllib.request.urlopen(self.url + path, timeout=3) as response:
                raw = response.read()
                self.assertEqual(response.status, 200)
                if path == '/':
                    self.assertIn(b'Prim Foundation', raw)
                    self.assertIn("default-src 'none'", response.headers['Content-Security-Policy'])
                else:
                    self.assertIsInstance(json.loads(raw), dict)

    def test_invalid_search_parameters_do_not_crash_server(self):
        import urllib.request, urllib.error
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(self.url + '/api/prims?limit=999999', timeout=3)
        self.assertEqual(caught.exception.code, 400)

    async def test_streamable_http_modern_and_legacy(self):
        for mode in ['auto','legacy']:
            async with Client(self.url+'/mcp',mode=mode,read_timeout_seconds=10) as client:
                result=await client.call_tool('prim_search',{'query':'research'})
                self.assertFalse(result.is_error)
                self.assertEqual(result.structured_content['items'][0]['id'],RESEARCH)

    def request_code(self,headers=None,body=None):
        import urllib.request,urllib.error
        payload=body or b'{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"test","version":"1"}}}'
        req=urllib.request.Request(self.url+'/mcp',data=payload,headers={'Content-Type':'application/json','Accept':'application/json, text/event-stream',**(headers or {})})
        try:
            with urllib.request.urlopen(req,timeout=3) as response:return response.status
        except urllib.error.HTTPError as exc:return exc.code

    def test_bad_host_rejected(self):
        self.assertEqual(self.request_code({'Host':'attacker.invalid'}),421)

    def test_bad_origin_rejected(self):
        self.assertEqual(self.request_code({'Origin':'https://attacker.invalid'}),403)

    def test_large_request_rejected(self):
        self.assertEqual(self.request_code(body=b'x'*70000),413)

    async def test_input_content_is_not_an_accepted_tool_parameter(self):
        async with Client(self.url+'/mcp',read_timeout_seconds=10) as c:
            tools=await c.list_tools()
            for tool in tools.tools:
                self.assertFalse({'record','data','content','vote','subject'} & set(tool.input_schema['properties']))


class GuardTests(unittest.IsolatedAsyncioTestCase):
    async def test_bounded_rate_and_client_map(self):
        from prim_library.guard import RequestGuard
        from starlette.responses import JSONResponse
        async def downstream(scope,receive,send):await JSONResponse({'ok':True})(scope,receive,send)
        guard=RequestGuard(downstream,per_minute=1,max_clients=1)
        statuses=[]
        async def send(m):
            if m['type']=='http.response.start':statuses.append(m['status'])
        async def receive():return {'type':'http.request','body':b''}
        scope={'type':'http','method':'GET','client':('127.0.0.1',1234),'headers':[]}
        await guard(scope,receive,send);await guard(scope,receive,send)
        await guard({**scope,'client':('127.0.0.2',1234)},receive,send)
        self.assertEqual(statuses,[200,429,429]);self.assertEqual(len(guard.counts),1)

class ExtraBoundaryTests(unittest.TestCase):
    def test_cyclic_local_schema_ref_rejected(self):
        schema={'$defs':{'a':{'$ref':'#/$defs/a'}},'$ref':'#/$defs/a'}
        with self.assertRaises(LibraryError):check_schema(schema)

    def test_stale_rankings_do_not_promote_profiles(self):
        r={'format':'prim-popularity','version':1,'as_of':'2000-01-01','profiles':{RESEARCH:{'stars':100,'status':'measured'}}}
        result=Library(rankings=r).search(sort='popular')
        research=next(x for x in result['items'] if x['id']==RESEARCH)
        self.assertEqual(research['popularity']['status'],'stale');self.assertEqual(research['popularity']['popular_score'],0)

    def test_historical_alias_is_searchable_not_an_identity_redirect(self):
        lib=Library();self.assertEqual(lib.search('orf')['items'][0]['id'],RESEARCH)
        with self.assertRaises(LibraryError):lib.get('orf')

    def test_xss_in_web_search_is_escaped(self):
        from prim_library.web import page
        output=page(Library().search(),query='<script>alert(1)</script>')
        self.assertNotIn('<script>',output);self.assertIn('&lt;script&gt;',output)


class CreationBoundaryTests(unittest.TestCase):
    def test_empty_nonobject_input_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(LibraryError):
                create(Library(), RESEARCH, RV, Path(root)/'record', [])


if __name__ == '__main__':
    unittest.main()

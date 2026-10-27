#!/usr/bin/env python3
"""Local proof of selected, scoped, approved GitHub-style research context.

This is a deterministic reference CLI, not a Grok Bot tool integration.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from who_exactly.knowledge import load_note, select_knowledge, validate_note


def main(argv=None):
    parser=argparse.ArgumentParser()
    sub=parser.add_subparsers(dest='cmd',required=True)
    sub.add_parser('validate')
    selection=sub.add_parser('select')
    selection.add_argument('--tags',required=True)
    selection.add_argument('--private-dir')
    selection.add_argument('--project-id')
    selection.add_argument('--max-notes',type=int,default=3)
    args=parser.parse_args(argv)
    public=ROOT/'knowledge'/'shared'
    if args.cmd=='validate':
        bad=[]
        for path in sorted(public.glob('*.md')):
            for error in validate_note(load_note(path)):
                bad.append(f'{path.relative_to(ROOT)}: {error}')
        if bad:
            print('\n'.join(bad),file=sys.stderr)
            return 1
        print(f'PASS: {len(list(public.glob("*.md")))} shared notes structurally valid')
        return 0
    selected=select_knowledge(public,tags=args.tags.split(','),project_dir=Path(args.private_dir) if args.private_dir else None,project_id=args.project_id,max_notes=args.max_notes)
    print(json.dumps({'status':'context_only_not_source_verification','notes':[{'id':n.metadata['id'],'scope':n.metadata['scope'],'status':n.metadata['status'],'path':str(n.path.relative_to(ROOT)) if n.path.is_relative_to(ROOT) else '[authorized-private]','score':n.score,'as_of':str(n.metadata['as_of'])} for n in selected]},indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())

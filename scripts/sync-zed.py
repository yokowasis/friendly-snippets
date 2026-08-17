import os
import sys
import json
import re
import copy
import subprocess

def load_json_with_comments(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Strip block comments /* ... */
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    # Strip line comments // ...
    lines = content.splitlines()
    clean_lines = []
    for line in lines:
        idx = line.find('//')
        if idx != -1:
            in_str = False
            for i in range(idx):
                if line[i] == '"' and (i == 0 or line[i-1] != '\\'):
                    in_str = not in_str
            if not in_str:
                line = line[:idx]
        clean_lines.append(line)
    cleaned = '\n'.join(clean_lines)
    # Strip trailing commas
    cleaned = re.sub(r',(\s*[\}\]])', r'\1', cleaned)
    try:
        return json.loads(cleaned)
    except Exception as e:
        print(f"Warning: Could not parse JSON from {filepath}: {e}")
        return {}

def main():
    # 1. Determine paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))
    friendly_dir = os.path.join(repo_root, "snippets")
    
    if not os.path.exists(friendly_dir):
        # Fallback to standard path
        friendly_dir = r"c:\Users\yokow\git\friendly-snippets\snippets"
        repo_root = r"c:\Users\yokow\git\friendly-snippets"

    appdata = os.environ.get("APPDATA") or os.path.expanduser("~")
    zed_dir = os.path.join(appdata, "Zed", "snippets")

    print(f"Friendly Snippets Source: {friendly_dir}")
    print(f"Zed Snippets Destination: {zed_dir}")

    pkg_json_path = os.path.join(repo_root, "package.json")
    file_default_scopes = {}
    if os.path.exists(pkg_json_path):
        with open(pkg_json_path, 'r', encoding='utf-8') as f:
            pkg = json.load(f)
        contributes = pkg.get('contributes', {}).get('snippets', [])
        for entry in contributes:
            rel_path = entry.get('path', '')
            fname = os.path.basename(rel_path)
            langs = entry.get('language', [])
            file_default_scopes[fname] = langs

    # Add default fallbacks for unmapped files
    file_default_scopes['github-actions-workflow.json'] = ['yaml']
    file_default_scopes['yaml.json'] = ['yaml']
    file_default_scopes['javascriptreact.json'] = ['javascriptreact', 'typescriptreact']

    # Map language scope -> target Zed snippet file(s)
    scope_to_zed_files = {
        'python': ['python.json'],
        'cpp': ['cpp.json'],
        'c': ['cpp.json'],
        'rust': ['rust.json'],
        'go': ['go.json'],
        'asm': ['go.json'],
        'markdown': ['markdown.json'],
        'latex': ['latex.json', 'tex.json'],
        'tex': ['latex.json', 'tex.json'],
        'javascript': ['javascript.json'],
        'typescript': ['typescript.json'],
        'javascriptreact': ['javascript.json', 'tsx.json'],
        'typescriptreact': ['tsx.json'],
        'jsx': ['javascript.json', 'tsx.json'],
        'tsx': ['tsx.json'],
        'html': ['html.json', 'php.json', 'svelte.json', 'tsx.json'],
        'php': ['php.json'],
        'svelte': ['svelte.json'],
        'shellscript': ['shellscript.json', 'shell script.json'],
        'bash': ['shellscript.json', 'shell script.json'],
        'sh': ['shellscript.json', 'shell script.json'],
        'mysql': ['mysql.json', 'sql.json'],
        'sql': ['sql.json', 'mysql.json'],
        'json': ['json.json'],
        'jsonc': ['jsonc.json'],
        'yaml': ['yaml.json'],
        'all': ['snippets.json'],
        'plaintext': ['snippets.json']
    }

    # Extract snippets by scope
    zed_files_clean = {}

    for fname in os.listdir(friendly_dir):
        if not fname.endswith(('.json', '.code-snippets')):
            continue
        fpath = os.path.join(friendly_dir, fname)
        data = load_json_with_comments(fpath)
        default_langs = file_default_scopes.get(fname, [])
        
        for snippet_name, snippet_def in data.items():
            if not isinstance(snippet_def, dict):
                continue
                
            if 'scope' in snippet_def and snippet_def['scope'].strip():
                raw_scope = snippet_def['scope']
                snippet_scopes = [s.strip() for s in raw_scope.split(',') if s.strip()]
            else:
                snippet_scopes = default_langs
                
            clean_snippet = copy.deepcopy(snippet_def)
            clean_snippet.pop('scope', None)
            
            for sc in snippet_scopes:
                target_zed_files = scope_to_zed_files.get(sc, [])
                for zf in target_zed_files:
                    if zf not in zed_files_clean:
                        zed_files_clean[zf] = {}
                    zed_files_clean[zf][snippet_name] = clean_snippet

    # Write files to Zed snippets directory
    os.makedirs(zed_dir, exist_ok=True)
    print("\nWriting files to Zed snippets directory...")
    for zf, sdict in sorted(zed_files_clean.items()):
        out_path = os.path.join(zed_dir, zf)
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(sdict, f, indent=4, ensure_ascii=False)
            f.write('\n')
        print(f"  - {zf}: {len(sdict)} snippets")

    # Format output JSON files with Prettier if available
    try:
        cmd = ["npx.cmd" if os.name == 'nt' else "npx", "-y", "prettier", "--tab-width", "4", "--parser", "json", "--write", os.path.join(zed_dir, "*.json")]
        subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("\nPrettier formatting applied to all Zed snippet files.")
    except Exception as e:
        print(f"\nSkipped prettier formatting: {e}")

    print("\nSynchronization complete!")

if __name__ == "__main__":
    main()

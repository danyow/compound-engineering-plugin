#!/usr/bin/env python3
"""
翻译指定的 references 文件为中文
直接替换原文件,保持代码块、技术术语不变
"""

import os
import sys
import re
from pathlib import Path

# 需要翻译的文件列表
AGENT_NATIVE_FILES = [
    "action-parity-discipline.md",
    "agent-execution-patterns.md", 
    "agent-native-testing.md",
    "architecture-patterns.md",
    "dynamic-context-injection.md",
    "files-universal-interface.md",
    "from-primitives-to-domain-tools.md",
    "mcp-tool-design.md",
    "mobile-patterns.md",
    "product-implications.md",
    "refactoring-to-prompt-native.md",
    "self-modification.md",
    "shared-workspace-architecture.md",
    "system-prompt-design.md"
]

ANDREW_KANE_FILES = [
    "testing-patterns.md",
    "rails-integration.md",
    "database-adapters.md",
    "resources.md",
    "module-organization.md"
]

BASE_PATH = Path("/home/runner/work/compound-engineering-plugin/compound-engineering-plugin/plugins/compound-engineering/skills")

def get_file_list():
    """获取所有需要翻译的文件路径"""
    files = []
    
    # agent-native-architecture
    agent_path = BASE_PATH / "agent-native-architecture" / "references"
    for f in AGENT_NATIVE_FILES:
        files.append(agent_path / f)
    
    # andrew-kane-gem-writer
    andrew_path = BASE_PATH / "andrew-kane-gem-writer" / "references"
    for f in ANDREW_KANE_FILES:
        files.append(andrew_path / f)
    
    return files

def main():
    files = get_file_list()
    
    print(f"需要翻译 {len(files)} 个文件:")
    for f in files:
        exists = "✓" if f.exists() else "✗"
        print(f"  {exists} {f.name}")
    
    print("\n这些文件需要使用 Claude API 进行翻译")
    print("由于文件较大,建议分批翻译")

if __name__ == "__main__":
    main()

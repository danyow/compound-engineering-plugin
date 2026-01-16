#!/usr/bin/env python3
"""
批量翻译 skills 目录中的 markdown 文件为中文
保持代码块、技术术语、URL、路径和 YAML frontmatter 键不变
"""

import os
import re
from pathlib import Path

# 不翻译的技术术语（保持英文）
TECHNICAL_TERMS = [
    'Agent', 'Command', 'Skill', 'Rails', 'React', 'TypeScript', 'Python', 'Ruby', 
    'JavaScript', 'Stimulus', 'Turbo', 'Hotwire', 'Figma', 'GitHub', 'PR', 'Issue',
    'MCP', 'YAML', 'JSON', 'ERB', 'API', 'CLI', 'SDK', 'DSPy', 'gem', 'npm',
    'HTML', 'CSS', 'Markdown', 'Git', 'worktree', 'TODO', 'CRUD', 'REST', 'HTTP',
    'Active Record', 'Gemini', 'OpenAI', 'Anthropic', 'Claude', 'Ollama', 'Haiku',
    'Sonnet', 'Opus', 'Minitest', 'RSpec', 'Bash', 'shell', 'regex', 'SQL',
    'PostgreSQL', 'Redis', 'Sidekiq', 'Tailwind', 'Docker', 'Kubernetes',
    'AWS', 'S3', 'Cloudflare', 'R2', 'rclone', 'base64', 'JPEG', 'PNG',
    'KISS', 'DRY', 'SOLID', 'TDD', 'CI/CD', 'DevOps'
]

def translate_content(text: str) -> str:
    """
    翻译 markdown 内容，保持代码块和技术术语不变
    这个函数目前只是占位符 - 实际翻译需要手动完成或使用 LLM API
    """
    # 这里应该调用 Claude API 进行翻译
    # 为了演示，我们只返回原文
    return text

def should_translate_file(file_path: Path) -> bool:
    """判断文件是否需要翻译"""
    # 只翻译 .md 文件
    return file_path.suffix == '.md'

def process_markdown_file(file_path: Path):
    """处理单个 markdown 文件"""
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分离 YAML frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        body = frontmatter_match.group(2)
        
        # 翻译主体内容（保持 frontmatter 键不变，只翻译值）
        translated_body = translate_content(body)
        
        # 重新组合
        translated_content = f"---\n{frontmatter}\n---\n{translated_body}"
    else:
        translated_content = translate_content(content)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(translated_content)
    
    print(f"✓ Translated: {file_path}")

def main():
    skills_dir = Path(__file__).parent / 'plugins/compound-engineering/skills'
    
    # 遍历所有 markdown 文件
    md_files = list(skills_dir.rglob('*.md'))
    
    print(f"Found {len(md_files)} markdown files")
    
    for md_file in md_files:
        if should_translate_file(md_file):
            process_markdown_file(md_file)

if __name__ == '__main__':
    main()

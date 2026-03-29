#!/usr/bin/env python3
"""
Skill 校验脚本
验证 skills/ 目录下的所有 Skill 是否符合规范
"""

import os
import sys
import re
import yaml
from pathlib import Path


def validate_frontmatter(skill_path):
    """验证 YAML frontmatter"""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, f"缺少 SKILL.md 文件"

    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否存在 frontmatter
    if not content.startswith('---'):
        return False, "SKILL.md 必须以 YAML frontmatter 开头 (---)"

    # 解析 frontmatter
    try:
        # 找到第一个 --- 和第二个 --- 之间的内容
        first_divider = content.find('---')
        second_divider = content.find('---', first_divider + 3)
        if second_divider == -1:
            return False, "YAML frontmatter 未正确关闭"

        fm_content = content[first_divider + 3:second_divider].strip()
        frontmatter = yaml.safe_load(fm_content)

        if frontmatter is None:
            return False, "YAML frontmatter 为空"

        # 验证必需字段
        required_fields = ['name', 'description', 'keywords']
        for field in required_fields:
            if field not in frontmatter:
                return False, f"缺少必需字段: {field}"

        # 验证 name
        if not isinstance(frontmatter['name'], str):
            return False, "name 必须是字符串"

        # 验证 description
        if not isinstance(frontmatter['description'], str):
            return False, "description 必须是字符串"
        if len(frontmatter['description']) < 40:
            return False, f"description 必须 >= 40 字 (当前: {len(frontmatter['description'])})"

        # 验证 keywords
        if not isinstance(frontmatter['keywords'], list):
            return False, "keywords 必须是数组"
        if len(frontmatter['keywords']) == 0:
            return False, "keywords 不能为空"

        return True, "OK"

    except yaml.YAMLError as e:
        return False, f"YAML 解析错误: {e}"
    except Exception as e:
        return False, f"验证错误: {e}"


def validate_structure(skill_path):
    """验证目录结构"""
    # 检查是否包含禁止的文件
    forbidden_files = ['README.md']
    for forbidden in forbidden_files:
        if (skill_path / forbidden).exists():
            return False, f"禁止包含 {forbidden} 文件"

    return True, "OK"


def validate_skill_name(skill_path):
    """验证 Skill 名称与目录名一致"""
    skill_md = skill_path / "SKILL.md"
    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 name
    match = re.search(r'^---\s*\nname:\s*(.+?)\s*\n', content, re.MULTILINE)
    if not match:
        return False, "无法提取 name 字段"

    name = match.group(1).strip()
    dir_name = skill_path.name

    # 名称应该与目录名匹配（kebab-case）
    if name != dir_name:
        return False, f"Skill name '{name}' 与目录名 '{dir_name}' 不匹配"

    return True, "OK"


def main():
    script_dir = Path(__file__).parent
    # 优先查找 MUXI/skills，兼容旧路径 skills/
    muxiskills_dir = script_dir.parent / "MUXI" / "skills"
    old_skills_dir = script_dir.parent / "skills"

    if muxiskills_dir.exists():
        skills_dir = muxiskills_dir
    elif old_skills_dir.exists():
        skills_dir = old_skills_dir
    else:
        print(f"错误: skills/ 目录不存在")
        print(f"  - 检查路径: {muxiskills_dir}")
        print(f"  - 备选路径: {old_skills_dir}")
        sys.exit(1)

    # 获取所有技能目录
    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]

    if not skill_dirs:
        print("警告: skills/ 目录下没有 Skill")
        sys.exit(0)

    print(f"校验 {len(skill_dirs)} 个 Skill...\n")

    all_valid = True
    for skill_dir in sorted(skill_dirs):
        print(f"检查: {skill_dir.name}")

        # 1. 验证 YAML frontmatter
        valid, msg = validate_frontmatter(skill_dir)
        if not valid:
            print(f"  ✗ frontmatter: {msg}")
            all_valid = False
            continue

        # 2. 验证目录结构
        valid, msg = validate_structure(skill_dir)
        if not valid:
            print(f"  ✗ 目录结构: {msg}")
            all_valid = False
            continue

        # 3. 验证名称一致性
        valid, msg = validate_skill_name(skill_dir)
        if not valid:
            print(f"  ✗ 名称: {msg}")
            all_valid = False
            continue

        print(f"  ✓ 通过")

    print()
    if all_valid:
        print("所有 Skill 校验通过!")
        sys.exit(0)
    else:
        print("存在校验失败的 Skill")
        sys.exit(1)


if __name__ == "__main__":
    main()
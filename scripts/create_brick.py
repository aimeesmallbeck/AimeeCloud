#!/usr/bin/env python3
"""
Brick Generator Script

Creates a new Arduino Brick from the template.

Usage:
    python3 create_brick.py --name my_brick --class MyBrick \\
        --description "My awesome brick" --category hardware
"""

import argparse
import os
import shutil
import re
from pathlib import Path


def camel_to_snake(name):
    """Convert CamelCase to snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_camel(name):
    """Convert snake_case to CamelCase."""
    return ''.join(word.capitalize() for word in name.split('_'))


def create_brick(args):
    """Create a new brick from template."""
    
    # Paths
    workspace_dir = Path(os.getenv('AIMEE_ROBOT_WS', '~/aimee-robot-ws')).expanduser()
    template_dir = workspace_dir / 'src/aimee_brick_template/brick_template'
    target_dir = workspace_dir / f'src/aimee_{args.name}'
    
    if not template_dir.exists():
        print(f"Error: Template directory not found: {template_dir}")
        return 1
        
    if target_dir.exists():
        print(f"Error: Brick already exists: {target_dir}")
        return 1
        
    # Create directory structure
    print(f"Creating brick: {args.name}")
    print(f"Target directory: {target_dir}")
    
    # Copy template
    shutil.copytree(template_dir, target_dir)
    
    # Rename template directory
    template_subdir = target_dir / 'src/arduino/app_bricks/template'
    brick_subdir = target_dir / f'src/arduino/app_bricks/{args.name}'
    template_subdir.rename(brick_subdir)
    
    # Replace placeholders in files
    replacements = {
        '{BRICK_NAME}': args.name,
        '{BrickClassName}': args.class_name,
        '{BRICK_DESCRIPTION}': args.description,
        '{BRICK_DISPLAY_NAME}': args.display_name or snake_to_camel(args.name).replace('_', ' '),
        '{BRICK_CATEGORY}': args.category,
        '{BRICK_FUNCTIONALITY}': args.functionality or args.description,
    }
    
    # Process all files
    for filepath in target_dir.rglob('*'):
        if filepath.is_file():
            # Rename files with template in name
            if 'template' in filepath.name:
                new_name = filepath.name.replace('template', args.name)
                filepath.rename(filepath.parent / new_name)
                filepath = filepath.parent / new_name
                
            # Replace content
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                for old, new in replacements.items():
                    content = content.replace(old, new)
                    
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except (UnicodeDecodeError, IOError):
                # Skip binary files
                pass
                
    print(f"✓ Brick '{args.name}' created successfully!")
    print(f"\nNext steps:")
    print(f"  1. Edit files in: {target_dir}")
    print(f"  2. Implement functionality in: {brick_subdir}/{args.name}.py")
    print(f"  3. Update config: {brick_subdir}/brick_config.yaml")
    print(f"  4. Build: cd {workspace_dir} && colcon build --packages-select aimee_{args.name}")
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='Create a new Arduino Brick for Aimee Robot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Create a hardware control brick
    python3 create_brick.py --name wake_word_ei \\
        --class WakeWordBrick \\
        --description "Edge Impulse wake word detection" \\
        --category audio
        
    # Create a sensor brick
    python3 create_brick.py --name battery_monitor \\
        --class BatteryMonitor \\
        --description "INA219 battery monitoring" \\
        --category sensors
        """
    )
    
    parser.add_argument(
        '--name', '-n',
        required=True,
        help='Brick name (snake_case, e.g., "my_brick")'
    )
    
    parser.add_argument(
        '--class', '-c',
        dest='class_name',
        required=True,
        help='Class name (CamelCase, e.g., "MyBrick")'
    )
    
    parser.add_argument(
        '--description', '-d',
        required=True,
        help='Short description of the brick'
    )
    
    parser.add_argument(
        '--category',
        default='general',
        choices=['hardware', 'audio', 'vision', 'sensors', 'network', 'general'],
        help='Brick category (default: general)'
    )
    
    parser.add_argument(
        '--display-name',
        help='Display name (default: derived from brick name)'
    )
    
    parser.add_argument(
        '--functionality',
        help='Detailed functionality description'
    )
    
    args = parser.parse_args()
    
    return create_brick(args)


if __name__ == '__main__':
    exit(main())

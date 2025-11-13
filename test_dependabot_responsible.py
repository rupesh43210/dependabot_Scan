import sys
from pathlib import Path

sys.path.insert(0, str(Path('.') / 'src'))

from reporters.security_report_generator import SecurityReportGenerator

gen = SecurityReportGenerator()

print('Testing get_responsible() for Dependabot reports:')
print(f'RQA: {gen.get_responsible("RQA")}')
print(f'tda-backend: {gen.get_responsible("tda-backend")}')
print(f'MiDAS-Platform: {gen.get_responsible("MiDAS-Platform")}')
print(f'Model_serving_platform: {gen.get_responsible("Model_serving_platform")}')

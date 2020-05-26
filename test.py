import sys
from pathlib import Path
current_file_path = Path(__file__)
sys.path.append(str(current_file_path.parent))

sys.argv.append('/Users/rajaravivarma')
import file_server

file_server.main()

print('hi')


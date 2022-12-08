
class Folder:
    def __init__(self, name):
        self.name = name
        self.full_path = None
        self.subfolders = {}
        self.files = {}
        self.parent = None

    def get_total_size(self):
        file_sizes = sum([self.files[x].size for x in self.files])
        sub_dir_sizes = sum([self.subfolders[x].get_total_size() for x in self.subfolders])
        return file_sizes + sub_dir_sizes

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = int(size)

def parse_input():
    #with open('inputs/day07.test.txt') as f:
    with open('inputs/day07.txt') as f:
        cmds = [x.strip('\n') for x in f.readlines()]
    root = None
    cwd = None
    for cmd in cmds:
        if cmd[0] == '$':
            # directory command, nuke previous cmd
            if cmd == '$ cd /':
                # let's start things off
                root = Folder('/')
                root.full_path = '/'
                cwd = root
            elif cmd == '$ cd ..':
                cwd = cwd.parent
            elif cmd == '$ ls':
                continue
            else:
                cwd = cwd.subfolders[cmd.split('cd ')[-1]]
        else: #not a command, so results of ls
            first, second = cmd.split()
            if first == 'dir':
                if second in cwd.subfolders:
                    print("oh shit")
                cwd.subfolders[second] = Folder(second)
                cwd.subfolders[second].parent = cwd
                cwd.subfolders[second].full_path = cwd.full_path + second + '/'
            else:
                if second in cwd.files:
                    print("oh snap")
                cwd.files[second] = File(second, first)
    return root

                
        

if __name__ == '__main__':
    root = parse_input()
    folder_dict = {}
    queue = [root]
    while queue:
        f = queue.pop()
        if f.name not in folder_dict:
            folder_dict[f.full_path] = f.get_total_size()
            queue.extend([f.subfolders[x] for x in f.subfolders])
    small = {key:value for (key, value) in folder_dict.items() if value <= 100000}
    print('part 1:', sum([small[x] for x in small]))
    
    total_disk_space = 70000000
    total_size = root.get_total_size()
    unused_space = total_disk_space - total_size
    needed_space = 30000000 - unused_space
    big = {key:value for (key, value) in folder_dict.items() if value > needed_space}
    print('part 2:', big[min(big, key=big.get)])
    #print(big)

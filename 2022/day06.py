
def parse_buffer(b, required_length=4):
    for i in range(required_length, len(b)):
        if len(set(b[i-required_length:i])) == required_length:
            break
    return i
        

if __name__ == '__main__':
    #with open('inputs/day06.test.txt') as f:
    with open('inputs/day06.txt') as f:
        buffers = [x.strip('\n') for x in f.readlines()]
    
    #[print(parse_buffer(x, 14)) for x in buffers]
    print('part 1:', parse_buffer(buffers[0], 4))
    print('part 2:', parse_buffer(buffers[0], 14))

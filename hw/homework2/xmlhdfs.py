from lxml import etree
import datetime
import sys
import re

fsimage_cl = sys.argv[1]
dir_cl = sys.argv[2]

def xmlhdfs_simulation(fsimage, data_dir):
    """
    Simulates the output of hdfs dfs -ls by formatting information from an xml document.

    Keyword Arguments:
    fsimage -- an xml document that contains NameNode information from hdfs
    dir -- a specific directory within a the xml document to output.

    Returns:
    The same output as hdfs dfs -ls: 1) the number of items in dir, 2) information about each item 3) sorted by file size
    """
    tree = etree.parse(open(fsimage))
    directories = data_dir.split('/')[1:]
    counter = 0
    try:                                        # Ensure that a single directory search has id or '/'
        exact_id = tree.xpath('/fsimage/INodeSection/inode[name = ' + '"' + directories[0] + '"' + ']/id/text()')[0]
    except IndexError:
        print('ls:' + data_dir + ': No such file or directory')
        return
    info_rows = []
    for dir_ in directories:
        try:
            parent_id = tree.xpath('/fsimage/INodeSection/inode[name = ' + '"' + dir_ + '"' + ']/id/text()')
            if len(parent_id) > 1:              # Deals with case when there are multiple files with same name.
                parent_id = tree.xpath('/fsimage/INodeSection/inode[id = ' + '"' + exact_id + '"' + ']/id/text()')[0]
            else:
                parent_id = parent_id[0]
        except IndexError:                      # Either there were multiple intial directories with same name OR file does not exist.
            print('ls:' + data_dir + ': No such file or directory')
            return

        next_num = counter + 1
        if (next_num) == len(directories):      # All directories have been searches.
            type_ = tree.xpath('/fsimage/INodeSection/inode[id = ' + '"' + exact_id + '"' + ']/type/text()')[0]
            if type_ == "FILE":
                type_indicator = '-'
                replication = tree.xpath('/fsimage/INodeSection/inode[id = ' + '"' + exact_id + '"' + ']/replication/text()')[0]
                permission = tree.xpath('/fsimage/INodeSection/inode[id = ' + '"' + exact_id + '"' + ']/permission/text()')[0]
                permission_split = permission.split(':')
                user_id = permission_split[0]
                group_id = permission_split[1]
                mode = permission_split[2][1:]
                mode_bits = calc_mode_bits(type_indicator, mode)
                file_size_lst = tree.xpath('/fsimage/INodeSection/inode[id = ' + '"' + exact_id + '"' + ']/blocks/block/numBytes/text()')
                file_size = 0
                for size in file_size_lst:
                    file_size += int(size)
                mtime_unformatted = tree.xpath('/fsimage/INodeSection/inode[id = ' + '"' + exact_id + '"' + ']/mtime/text()')[0]
                mtime_formatted = str(datetime.datetime.fromtimestamp(int(mtime_unformatted)/1e3))
                mtime = re.search('.*:.*:', mtime_formatted).group(0)[0:-1]

                info_rows.append([mode_bits, replication, user_id, group_id, file_size, mtime, data_dir])
            else:
                children_ids = tree.xpath('/fsimage/INodeDirectorySection/directory[parent = ' + exact_id + ']/child/text()')
                id_to_bytes_d = {}
                for id_ in children_ids:
                    file_size_lst = tree.xpath('/fsimage/INodeSection/inode[id = ' + '"' + id_+ '"' + ']/blocks/block/numBytes/text()')
                    id_to_bytes_d[id_] = 0
                    for size in file_size_lst: 
                        id_to_bytes_d[id_] = id_to_bytes_d[id_] + int(size)

                id_to_bytes_d = sorted(id_to_bytes_d.items(), key=lambda x: x[1])
                if len(children_ids) > 1:
                    print('Found ' + str(len(children_ids)) + ' items')
                for id_bytes in id_to_bytes_d:
                    id_ = id_bytes[0]
                    file_size = id_bytes[1]
                    type_ = tree.xpath('/fsimage/INodeSection/inode[id = ' + '"' + id_ + '"' + ']/type/text()')[0]
                    if type_ == "FILE":
                        type_indicator = '-'
                    else:
                        type_indicator = 'd'
                    try:
                        replication = tree.xpath('/fsimage/INodeSection/inode[id = ' + '"' + id_ + '"' + ']/replication/text()')[0]
                    except IndexError:
                        replication = '-'

                    permission = tree.xpath('/fsimage/INodeSection/inode[id = ' + '"' + id_ + '"' + ']/permission/text()')[0]
                    permission_split = permission.split(':')
                    user_id = permission_split[0]
                    group_id = permission_split[1]
                    mode = permission_split[2][1:]
                    mode_bits = calc_mode_bits(type_indicator, mode)
                    mtime_unformatted = tree.xpath('/fsimage/INodeSection/inode[id = ' + '"' + id_ + '"' + ']/mtime/text()')[0]
                    mtime_formatted = str(datetime.datetime.fromtimestamp(int(mtime_unformatted)/1e3))
                    mtime = re.search('.*:.*:', mtime_formatted).group(0)[0:-1]
                    name = tree.xpath('/fsimage/INodeSection/inode[id = ' + '"' + id_ + '"' + ']/name/text()')[0]

                    if data_dir == '/':
                        directory = data_dir + name
                    else:
                        directory = data_dir + '/' + name

                    info_rows.append([mode_bits, replication, user_id, group_id, file_size, mtime, directory])
            print_row(info_rows)                    
            return

        children_ids = tree.xpath('/fsimage/INodeDirectorySection/directory[parent = ' + parent_id + ']/child/text()')
        if not children_ids:                    # No children IDs, kill the search.
            print('ls:' + data_dir + ': No such file or directory')
            return
        else:
            dir_next = directories[next_num]
            try:
                next_id = tree.xpath('/fsimage/INodeSection/inode[name = ' + '"' + dir_next + '"' + ']/id/text()')
                if len(next_id) > 1:
                    for id_ in next_id:
                        if id_ in children_ids:
                            next_id = id_
                else:
                    next_id = next_id[0]
            except IndexError:                  # Could not find a matching ID from potential IDs that is in children IDs.
                print('ls:' + data_dir + ': No such file or directory')
                return

            if next_id in children_ids:         # Ensure the next_id is in list of children IDs.
                counter += 1
                exact_id = next_id
                continue
            else:
                print('ls:' + data_dir + ': No such file or directory')
                return
    return

def calc_mode_bits(mode_bits, mode):
    """ Calculates the mode_bits based on the permission mode """
    int_to_octave = {'0': '000', '1': '001', '2': '010', '3': '011', '4': '100', '5': '101', '6': '110', '7': '111'}
    octave_to_rwx = {'000': '---', '001': '--x', '010': '-w-', '011': '-wx', '100': 'r--', '101': 'r-x', '110': 'rw-', '111': 'rwx'}

    for int_ in mode:
        mode_bits += octave_to_rwx[int_to_octave[int_]]

    return mode_bits

def print_row(rows):
    """ Prints the Rows so that they are tabularly separated and aligned to the right """
    max_d = {}
    for i in range(len(rows[0])):
        max_d[i] = find_max_len(rows, i)
    for line in rows:
        final = line[0].rjust(max_d[0]) + '\t' + line[1].rjust(max_d[1]) + '\t' + line[2].rjust(max_d[2]) + '\t' + line[3].rjust(max_d[3]) + '\t' + str(line[4]).rjust(max_d[4]) + '\t' + line[5].rjust(max_d[5]) + '\t' + line[6].rjust(max_d[6])
        print(final)

def find_max_len(rows, row_num):
    """ Helper function to print rows to find the max length of each of the 7 information pieces """
    max_ = 0
    for line in rows:
        if max_ == 0:
            max_ = len(str(line[row_num]))
        elif len(str(line[row_num])) > max_:
            max_ = len(str(line[row_num]))
    return max_

def printf(elems):
    """ Helper function to print tree """
    if (isinstance(elems, list)):
        for elem in elems:
            if isinstance(elem, str):
                print(elem)
            else:
                print(etree.tostring(elem, pretty_print=True))
    else: # just a single element
        print(etree.tostring(elems))

xmlhdfs_simulation(fsimage_cl, dir_cl)




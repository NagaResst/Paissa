import csv

with open('item.csv', 'r', encoding='utf8') as item_file:
    item_in_list = csv.DictReader(item_file)
    item_out_list = []
    for i in item_in_list:
        # print(i)
        if i['16'] != '0' and i['0'] != '':
            item = {'ID': i['\ufeffkey'], 'Name': i['0'], 'Icon': i['10']}
            # print(item)
            item_out_list.append(item)

# print(item_out_list, len(item_out_list))
if item_out_list[0]['ID'] == '#':
    del item_out_list[0]
if item_out_list[0]['ID'] == 'int32':
    del item_out_list[0]
# print(item_out_list)
with open('item.Pdt', 'w', encoding='utf8') as item_data:
    item_data.write(str(item_out_list))

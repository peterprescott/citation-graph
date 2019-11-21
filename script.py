import os.path
import sys
import reader
import literature as lit

if __name__ == '__main__':
    print('running')
    starting_key = 'RWebberBurrows2018'
    get = reader.Bib(starting_key)
    ref_data = get.references()
    # ~ print(ref_data.entries)
    db_file=os.path.join(sys.path[0], 'citation_graph.db')
    texts = []
    for entry in ref_data.entries:
        # ~ key = entry
        # ~ title = str(ref_data.entries[entry].fields['title']).replace('}','').replace('{','')
        # ~ creators = ref_data.entries[entry].persons
        # ~ creators_list = []
        # ~ for creator_type in creators:
            # ~ for creator in creators[creator_type]:
                # ~ surname = creator.last_names[0]
                # ~ initial = creator.first_names[0][0]
                # ~ creators_list.append({"surname" : surname, 
                                    # ~ "initial" : initial, 
                                    # ~ "role" : creator_type})
        # ~ year = str(ref_data.entries[entry].fields['year']).replace('}','').replace('{','')
        text_type = ref_data.entries[entry].type
        # ~ texts.append(lit.Text(db_file, key, year, title, text_type, creators=creators_list))
        if text_type == "book":
            print(ref_data.entries[entry])
            publisher = ref_data.entries[entry].fields['address']
            location = ref_data.entries[entry].fields['publisher']
            number_of_pages = "unknown"
            isbn = ref_data.entries[entry].fields['isbn']

"""
    XML standard python package - reads the xml file entirely
    into the memory
"""
# import xml.etree.ElementTree as ET

# tree = ET.parse('orders.xml')
# root = tree.getroot()
# element_tag = root.tag
# element_attrib = root.attrib

# print(element_tag)
# print(element_attrib)

# cnt = 0
# for child in root:
    
#     order_type = child.tag
#     book = child.get('book')
#     operation = child.get('operation')
#     price = child.get('price')
#     volume = child.get('volume')
#     orderId = child.get('orderId')

#     print(f"cnt = {cnt}, {order_type,book,operation,price,volume,orderId}")

#     cnt += 1
#     if cnt == 5:
#         break

"""
    LXML - Event driven parsing - reads data incrementally and 
    doesn't load the entire XML file into memory
"""
from lxml import etree

# Specify the path to your large XML file
xml_file_path = "orders.xml"

# Create an event-driven parser
context = etree.iterparse(xml_file_path, events=("start", "end"))

# Initialize variables to store data
data, data2 = [], []

# for event, element in context:
#     if event == "start":
#         # Process the element at the start of a tag
#         if element.tag == "AddOrder":
#             # Extract and process the data within the element
#             # element_data = element.text
#             price = element.get("price")
#             # Store the data in your data structure or perform further processing
#             data.append(price)
#         else:
#             orderId = element.get("orderId")
#             data2.append(orderId)

#     if event == "end":
#         # Clear the element from memory to save memory
#         element.clear()

# # Release resources
# del context

# Now, you can work with the 'data' list, which contains the extracted data
# for item in data:
#     print(item)

def get_val(x):
    print(x)
    return None

while port := get_val(5) and port <= 10:
    print(port)
    port += 1
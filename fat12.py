import binascii
import time

filename = 'image.dat'
with open(filename, 'rb') as f:
    content = f.read()
    
data = binascii.hexlify(content)
bytes = [data[k:k+2] for k in range(0, len(data), 2)]


def hex_to_ascii(h):
	ascii = ''.join(h).decode("hex")
	return ascii

def hex_to_dec_str(h):
	string = ''.join(h[::-1])
	dec = int(string, 16);
	return str(dec)

def hex_to_decimal(h):
	string = ''.join(h[::-1])
	dec = int(string, 16);
	return dec

device_name = bytes[43:54]
print('Device name: ' + hex_to_ascii(device_name))
serial_number = bytes[39:43]
print('Serial number: ' + hex_to_dec_str(serial_number))

filesystem_type = bytes[54:62]
print('Filesystem type: ' + hex_to_ascii(filesystem_type))

media_desc = bytes[21:22]
print('Media descriptor type: '+str(media_desc[0]))

bytes_per_sector = bytes[11:13]
print('Bytes per sector: ' + hex_to_dec_str(bytes_per_sector))

nbr_reserved_sectors = bytes[14:16]
print('Number of reserved sectors: ' + hex_to_dec_str(nbr_reserved_sectors))


nbr_sectors_per_allocation = bytes[13:14]
print('Number of sectors per allocation/cluster: ' + hex_to_dec_str(nbr_sectors_per_allocation))

nbr_sectors_per_FAT = bytes[22:24]
print('Number of sectors per FAT: ' + hex_to_dec_str(nbr_sectors_per_FAT))

nbr_sectors_per_track = bytes[24:26]
print('Number of sectors per track: ' + hex_to_dec_str(nbr_sectors_per_track))

nbr_heads_on_diskette = bytes[26:28]
print('Number of heads on diskette: ' + hex_to_dec_str(nbr_heads_on_diskette))

nbr_hidden_sectors = bytes[28:32]
print('Number of hidden sectors: ' + hex_to_dec_str(nbr_hidden_sectors))

start_of_bootstrap_routine = bytes[0:3]
print('Start of bootstrap routine: ' + hex_to_dec_str(start_of_bootstrap_routine))

nbr_of_FATs = bytes[16:17]
print('Number of FATs: ' + hex_to_dec_str(nbr_of_FATs))

boot_signature = bytes[38:39]
print('Boot signature: ' + hex_to_dec_str(boot_signature))

size_of_device = bytes[19:21]
print('Size of device: ' + str(512*hex_to_decimal(size_of_device)))

offset_to_start_of_FATs = hex_to_dec_str(bytes_per_sector)
print('Offset to start of FATs: ' + offset_to_start_of_FATs)

root_dir_offset = hex_to_decimal(bytes_per_sector)*19
print('Root directory offset: ' + str(root_dir_offset))

offset_to_data_area = hex_to_decimal(bytes_per_sector)*33
print('Offset to data area: ' + str(offset_to_data_area))

#Visualize fat table:

def parse_fat_entry(entry):
	entry_text = '';

	if (entry[0:2] == '00'):
		entry_text = '[Unused] '
	elif entry >= 'ff0' and entry <= 'ff6':
		entry_text = '[Reserved Cluster] '
	elif entry == 'ff7':
		entry_text = '[BAD Cluster] '
	elif entry >= 'ff8' and entry <= 'fff':
		entry_text = '[Last cluster in file] '
		print(entry_text + entry)
	else:
		entry_text = '[Next cluster] '

	entry_text += entry;
	return entry_text;

def extract_fat_entry(offset, n):
	fat=0
	if(n%2==0):
		high=bytes[offset+1+(3*n)/2][1]
		low=bytes[offset+(3*n)/2]
		fat=high+low

	else:
		low=bytes[offset+1+(3*n)/2][0]
		high=bytes[offset+(3*n)/2]
		fat=high+low

#	print("Low: "+low)
#	print("High: "+high)
	if fat in ['200','400','600','800','a00','c00','e00']:
		fat='000'
	return fat

def parse_date(date):
	timestr=''.join(date)
	print(timestr)
	return " "

def parse_time(time):
	time=0
	return " "
	
def read_root_dir():
	i=root_dir_offset
	stop=offset_to_data_area
	while (i<stop):
		data = bytes[i:i+32]
		filename=data[0:8]
		extension=data[8:11]
		attributes=data[11:12]
		reserved=data[12:14]
		creation_time=data[14:16]
		creation_date=data[16:18]
		last_write_time=data[22:24]
		last_write_date=data[24:26]
		first_logical_cluster=data[26:28]
		file_size=data[28:32]
		
		i=i+32;
		
		#if filename[0] not in ['e5','00']:
		if filename[0] not in ['zz','xx']:
			print("---------------------------")
			print("Filename:"+hex_to_ascii(filename))
			#print("0x"+str(filename))
			print("Extension:"+hex_to_ascii(extension))
			print("Attributes:"+''.join(attributes))
			print("Reserved:"+''.join(reserved))
			print("Creation time:"+parse_time(creation_time))
			print("Creation date:"+parse_date(creation_date))
			print("Last write time:"+hex_to_dec_str(last_write_time))
			print("Last write date:"+hex_to_dec_str(last_write_date))
			print("First logical cluster:"+hex_to_dec_str(first_logical_cluster))
			print("File size:"+hex_to_dec_str(file_size))
			
for x in range(300):
	entry = extract_fat_entry(512, x)
	#print(parse_fat_entry(entry))
	#print(extract_fat_entry(512, x))
read_root_dir()

	





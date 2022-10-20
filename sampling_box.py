import nrrd
import argparse
import csv
import sys


def check_positive(number):
    if number <= 0:
        sys.exit('ERROR! The supplied number is 0 or negative. Only numbers greater than 0 are allowed.')


def read_nrrd(file):
    data, header = nrrd.read(file)

    return [data, header]


def read_csv(file):
    sample_positions = []
    with open(file) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        # next(reader, None)  # skip the header
        for row in reader:
            value_1 = int(row[0])
            value_2 = int(row[1])
            value_3 = int(row[2])

            sample_positions.append([value_1, value_2, value_3])

    return sample_positions


def check_coordinates(coordinates, data):
    for i in range(3):
        if coordinates[i] > data.shape[i]:
            sys.exit('ERROR! The supplied coordinates ' + str(coordinates) +
                     ' are outside the sample area. Choose coordinates inside sample area, dimensions of sample area '
                     + str(data.shape) + '.')


def create_sub_array(volume_image, coordinates, box):
    sample_box = volume_image[coordinates[0]-(box//2):coordinates[0]+(box//2),
                 coordinates[1]-(box//2):coordinates[1]+(box//2), coordinates[2]-(box//2):coordinates[2]+(box//2)]

    return sample_box


def check_box(coordinates, box, data):
    for i in range(3):
        if coordinates[i]-(box//2) < 0 or coordinates[i]+(box//2) > data.shape[i]:
            sys.exit('ERROR! The supplied box edge length ' + str(box) +
                     ' leads to sample box outside the sample area with dimensions '
                     + str(data.shape) + '. Choose smaller box edge length or different coordinates. '
                                         'Current coordinates are ' + str(coordinates) + '.')


def analyze_volume(sample_box):
    vessel = 0
    background = 0
    # Iterate through every array position
    for i in range(len(sample_box)):
        for j in range(len(sample_box[i])):
            for k in range(len(sample_box[i][j])):
                # Todo: support labels
                if sample_box[i, j, k] != 0:
                    vessel += 1
                else:
                    background += 1

    print('In the sample there are ' + str(vessel) + ' voxels of vessels and ' + str(background)
          + ' voxels of background.')

    fraction = round((vessel / (vessel + background)) * 100, 2)

    return [vessel, background, fraction]


def write_csv(data, file):
    if file is None:
        file = 'results'
    with open(file + '.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['voxels vessel', 'voxels background', 'fraction'])
        for entry in data:
            csv_writer.writerow(entry)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Calculate volume fractions for sample areas in volume image.')
    parser.add_argument('filename', action='store', type=str, help='Input file')
    parser.add_argument('csv', action='store', type=str, help='.csv file containing sampling locations')
    parser.add_argument('box_size', action='store', type=int, help='Edge length of sample box.')
    parser.add_argument('-o', '--output', action='store', type=str, help='Output file, if not provided '
                                                                         'results will be written to results.csv')

    args = parser.parse_args()

    nrrd_file_path = args.filename
    csv_file_path = args.csv
    box_edge_length = args.box_size
    output_file = args.output

    check_positive(box_edge_length)

    print('Reading .nrrd file')
    nrrd = read_nrrd(nrrd_file_path)

    nrrd_data = nrrd[0]
    nrrd_header_dimensions = nrrd[1]['sizes']
    print('Dimensions of sample area: ' + str(nrrd_header_dimensions))

    sample_coordinates = read_csv(csv_file_path)

    sampling_results = []

    for line in sample_coordinates:
        print('Checking coordinates.')
        check_coordinates(line, nrrd_data)

        print('Checking sample box.')
        check_box(line, box_edge_length, nrrd_data)

        print('Creating sample box.')
        sub_volume = create_sub_array(nrrd_data, line, box_edge_length)

        print('Analyzing sample box.')
        analysis_results = analyze_volume(sub_volume)
        sampling_results.append(analysis_results)

    print('Writing output.')
    write_csv(sampling_results, output_file)

import GeneticAlgorithm


def main():
    data_path = "./data/had12.dat"
    distances, flows = get_data(data_path)
    GeneticAlgorithm.run(distances, flows)


def get_data(data_path):
    out_distances = []
    out_flows = []
    with open(data_path, 'r') as data:
        number_of_facilities = int(data.readline().strip())
        i_distance = 0

        while i_distance < number_of_facilities:
            line = data.readline().strip()
            if line != "":
                if len(line.split()) < number_of_facilities:
                    raise IndexError
                out_distances.append(line.split())
                i_distance += 1

        i_flow = 0
        while i_flow < number_of_facilities:
            line = data.readline().strip()
            if line != "":
                if len(line.split()) < number_of_facilities:
                    raise IndexError
                out_flows.append(line.split())
                i_flow += 1

    return out_distances, out_flows


main()

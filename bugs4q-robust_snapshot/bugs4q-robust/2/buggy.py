from qiskit_machine_learning.datasets import ad_hoc_data
from qiskit.aqua.utils import split_dataset_to_data_and_labels

def run():
    feature_dim=2
    training_dataset_size=20
    testing_dataset_size=10
    random_seed=10598
    shots=10000

    sample_Total,training_input,test_input,class_labels = ad_hoc_data(training_size=training_dataset_size,
                                                                test_size=testing_dataset_size,
                                                                gap=0.3,
                                                                n=feature_dim,
                                                                plot_data=True)

    datapoints, class_to_label = split_dataset_to_data_and_labels(test_input)


if __name__ == '__main__':
    run()
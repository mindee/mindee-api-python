import statistics
import calendar
import json
import time
import os
from os import path
from mindee.plots import plot_metrics


class Benchmark(object):
    def __init__(
            self,
            output_dir,
            benchmark_name=None
    ):
        """
        :param output_dir: Directory path for saving benchmark results
        :param benchmark_name: Optional name of the benchmark folder inside output_dir
        """
        if not path.exists(output_dir):
            raise Exception(
                'Output directory %s does not exist. Please create it before running benchmark.' % output_dir)
        self.output_dir = output_dir
        self.results = None

        if benchmark_name is None:
            benchmark_name = str(calendar.timegm(time.gmtime()))

        self.benchmark_dir = os.path.join(self.output_dir, benchmark_name)
        os.mkdir(self.benchmark_dir)

        self.results_dir = os.path.join(self.output_dir, benchmark_name, "results")
        os.mkdir(self.results_dir)

    def initialize(self, result):
        """
        :param result: output from Document.compare method
        :return: (void) initialize benchmark results
        """
        self.results = {"file_ids": []}
        for key in result.keys():
            self.results[key] = []

    def add(self, result, file_id):
        """
        :param result: output from Document.compare method
        :param file_id: Unique file identifier
        :return: (void) add a data point to the benchmark
        """
        if self.results is None:
            self.initialize(result)

        assert set(result.keys()) == set(self.results.keys()) - {"file_ids"}
        for key in result.keys():
            if '__pre__' in key and result[key] is not None:
                self.results[key].append(result[key])
            if '__acc__' in key:
                self.results[key].append(result[key])

        self.results["file_ids"].append(file_id)

        with open(os.path.join(self.results_dir, '%s.json' % file_id), "w") as fp:
            json.dump(result, fp)

    def save(self):
        """
        :return: (void) plot precision and accuracy bar chart into output_dir folder
        """
        with open(os.path.join(self.benchmark_dir, 'results.json'), "w") as fp:
            json.dump(self.results, fp)

        metrics = []
        accuracies = []
        precisions = []
        for key in set(self.results.keys()) - {"file_ids"}:
            if "__acc__" in key:
                metrics.append(key[7:])
                accuracies.append(round(statistics.mean(self.results[key]) * 100, 2))
                precisions.append(round(statistics.mean(self.results['__pre__'+key[7:]]) * 100, 2))

        plot_metrics(metrics, accuracies, precisions, os.path.join(self.benchmark_dir, 'metrics.png'))

    @staticmethod
    def scalar_precision_score(field, ground_truth):
        """
        :param field: Field to compare
        :param ground_truth: Ground truth field to make the comparison on
        :return: True or False if the Field is set, None otherwise
        """
        if field.value is None:
            return None
        else:
            return field == ground_truth

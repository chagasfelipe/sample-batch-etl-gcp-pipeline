from __future__ import absolute_import
import argparse
import logging
import regex as re
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import os
from past.builtins import unicode
from apache_beam.io import ReadFromText, ReadAllFromText
from apache_beam.io import WriteToText
from apache_beam.metrics import Metrics
from apache_beam.metrics.metric import MetricsFilter
from apache_beam.options.pipeline_options import SetupOptions
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/chagas_felipe_1989/resources/desafio-engenheiro-de-dados-58fce9a588d4.json"

class DataIngestion:
    def parse_method(self, string_input):
        values = re.split(",", re.sub('\r\n', '', re.sub(u'"', '', string_input)))
        row = dict(
            zip(('component_id', 'component_type_id', 'type', 'connection_type_id', 'outside_shape', 'base_type', 'height_over_tube', 'bolt_pattern_long', 'bolt_pattern_wide', 'groove', 'base_diameter', 'shoulder_diameter', 'unique_feature', 'orientation', 'weight'),
                values))
        return row

def run(argv=None):

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--input',
        dest='input',
        required=False,
        default='gs://bucket-desafio-engenheiro-dados-data-lake/comp_boss.csv')

    parser.add_argument('--output',
                        dest='output',
                        required=False,
                        default='industrial_machine_product_data.tb_component')

    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_args.extend([
        '--project=desafio-engenheiro-de-dados',
        '--runner=DataflowRunner',
        '--staging_location=gs://bucket-desafio-engenheiro-dados-data-lake/staging',
        '--temp_location=gs://bucket-desafio-engenheiro-dados-data-lake/temp',
        '--requirements_file requirements.txt',
        '--region=us-east1'
    ])

    data_ingestion = DataIngestion()
    p = beam.Pipeline(options=PipelineOptions(pipeline_args))

    (
     p | 'Read from a File' >> beam.io.ReadFromText(known_args.input,
                                                  skip_header_lines=1)
    
     | 'String To BigQuery Row' >>
     beam.Map(lambda s: data_ingestion.parse_method(s))
     | 'Write to BigQuery' >> beam.io.Write(
        beam.io.WriteToBigQuery(
            known_args.output,
            custom_gcs_temp_location='gs://bucket-desafio-engenheiro-dados-data-lake/temp/',
            schema='component_id:STRING, component_type_id:STRING, type:STRING, connection_type_id:STRING, outside_shape:STRING, base_type:STRING, height_over_tube:STRING, bolt_pattern_long:STRING, bolt_pattern_wide:STRING, groove:STRING, base_diameter:STRING, shoulder_diameter:STRING, unique_feature:STRING, orientation:STRING, weight:STRING',
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE)))
    p.run().wait_until_finish()

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
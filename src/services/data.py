from flask import jsonify
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
from web3 import Web3
import requests

load_dotenv()

def query_txn_address(address, start_block=0):
    return (
        f"https://api.etherscan.io/api?module=account&action=txlist&address={
            address}&"
        f"startblock={
            start_block}&endblock=19999999&page=1&offset=10000&sort=asc&"
        f"apikey={os.getenv('ETHERSCAN_API_KEY')}"
    )


def fetch_data(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.json()['result']


def convert_columns(df, int_columns, float_columns):
    df[int_columns] = df[int_columns].astype(np.int64).fillna(0)
    df[float_columns] = df[float_columns].astype(np.float64).fillna(0)
    return df


def get_txs_by_address(address):
    try:
        columns_to_keep = ['from', 'to', 'contractAddress']
        int_columns = ['blockNumber', 'timeStamp', 'isError']
        float_columns = ['value', 'gasPrice',
                         'gas', 'cumulativeGasUsed', 'gasUsed']

        initial_url = query_txn_address(address)
        data = fetch_data(initial_url)

        df = pd.DataFrame(data)[columns_to_keep + int_columns + float_columns]

        # Loop through the data
        if len(df) == 10000:
            last_block_number = df['blockNumber'].iloc[-1]
            additional_url = query_txn_address(address, last_block_number)
            additional_data = fetch_data(additional_url)

            new_df = pd.DataFrame(additional_data)[
                columns_to_keep + int_columns + float_columns]
            df = pd.concat([df, new_df], ignore_index=True).drop_duplicates()

        df = convert_columns(df, int_columns, float_columns)

        return df.iloc[0].to_list()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()


def calculate_sent_stats(sample_df_grouped, time_dim, sent_stats):
    if 'sent' in sample_df_grouped.groups:
        sent_df = sample_df_grouped.get_group('sent')
        sent_df.loc[:, 'gas_fee'] = sent_df['gasPrice'] * sent_df['gasUsed']
        sent_df['gas_fee_eth'] = sent_df['gas_fee'].apply(
            lambda x: Web3.from_wei(int(x), 'ether'))

        sent_stats['avg_gas_fee'] = sent_df['gas_fee_eth'].mean()
        sent_stats['total_ether_sent'] = sent_df['eth_value'].sum()
        sent_stats['unique_sent'] = sent_df['to'].nunique()
        sent_stats['sent_tnx'] = len(sent_df)
        sent_stats['min_val_sent'] = sent_df['eth_value'].min()
        sent_stats['max_val_sent'] = sent_df['eth_value'].max()
        sent_stats['avg_val_sent'] = sent_df['eth_value'].mean()

        sent_stats['avg_min_sent'] = time_dim['sent']/len(sent_df)
    return sent_stats


def calculate_received_stats(sample_df_grouped, time_dim, received_stats):
    if 'received' in sample_df_grouped.groups:
        received_df = sample_df_grouped.get_group('received')

        received_stats['received_tnx'] = len(received_df)
        received_stats['min_value_received'] = received_df['eth_value'].min()
        received_stats['max_value_received'] = received_df['eth_value'].max()
        received_stats['avg_value_received'] = received_df['eth_value'].mean()
        received_stats['total_ether_received'] = received_df['eth_value'].sum()
        received_stats['unique_received'] = received_df['from'].nunique()
        received_stats['avg_min_received'] = time_dim['reviced'] / \
            len(received_df)

    return received_stats


def get_stats_normal_tnx(sample_df, address):
    address = address.lower()

    sample_df['eth_value'] = sample_df['value'].apply(
        lambda x: Web3.from_wei(int(x), 'ether'))

    sample_df['txn_type'] = np.where(
        sample_df['from'].str.lower() == address, 'sent', 'received')

    sample_df['unixTimeDiff'] = sample_df['timeStamp'].diff()
    time_dim = sample_df.groupby('txn_type')['unixTimeDiff'].sum()/60

    sample_df_grouped = sample_df.groupby('txn_type')

    sent_stats = {
        'min_gas_fee': 0,
        'max_gas_fee': 0,
        'avg_gas_fee': 0,
        'total_ether_sent': 0,
        'unique_sent': 0,
        'sent_tnx': 0,
        'min_val_sent': 0,
        'max_val_sent': 0,
        'avg_val_sent': 0,
        'avg_min_sent': 0
    }

    sent_stats = calculate_sent_stats(sample_df_grouped, time_dim, sent_stats)

    received_stats = {
        'received_tnx': 0,
        'min_value_received': 0,
        'max_value_received': 0,
        'avg_value_received': 0,
        'total_ether_received': 0,
        'unique_received': 0,
        'avg_min_received': 0
    }

    received_stats = calculate_received_stats(
        sample_df_grouped, time_dim, received_stats)

    overall_stats = {
        'address': address,
        'avg_sent_time': sent_stats['avg_min_sent'],
        'avg_received_time': received_stats['avg_min_received'],
        'time_difference_mins': (sample_df['timeStamp'].max() - sample_df['timeStamp'].min()) / 60,
        'sent': sent_stats['sent_tnx'],
        'received': received_stats['received_tnx'],
        'errors': len(sample_df[sample_df['isError'] != 0]),
        'unique_received_addresses': received_stats['unique_received'],
        'unique_sent_addresses': sent_stats['unique_sent'],
        'min_eth_received': received_stats['min_value_received'],
        'max_eth_received': received_stats['max_value_received'],
        'avg_eth_received': received_stats['avg_value_received'],
        'min_eth_sent': sent_stats['min_val_sent'],
        'max_eth_sent': sent_stats['max_val_sent'],
        'avg_eth_sent': sent_stats['avg_val_sent'],
        'avg_gas_fee': sent_stats['avg_gas_fee'],
        'total_txs': len(sample_df),
        'total_eth_sent': sent_stats['total_ether_sent'],
        'total_eth_received': received_stats['total_ether_received'],
    }

    return pd.DataFrame([overall_stats]).iloc[0].to_list()


def get_data(address):
    sample_df = get_txs_by_address(address)
    if len(sample_df) == 0:
        return jsonify({'error': 'No data found for the address'})

    return get_stats_normal_tnx(sample_df, address)

def get_address_stats_normal_tnx(sample_df, address):
    address = address.lower()
    
    sample_df['eth_value'] = Web3.from_wei(
        sample_df['value'].astype(int), 'ether')
    
    sample_df['txn_type'] = np.where(
        sample_df['from'].str.lower() == address, 'sent', 'received')
    
    sample_df['timeStamp'] = pd.to_datetime(sample_df['timeStamp'], unit='s')

    # Group by 'txn_type'
    sample_df_grouped = sample_df.groupby('txn_type')

    # Initialize statistics for sent transactions
    sent_stats = {
        'min_gas_fee': 0,
        'max_gas_fee': 0,
        'avg_gas_fee': 0,
        'total_ether_sent': 0,
        'unique_sent_to_addresses': 0,
        'sent_tnx': 0,
        'min_val_sent': 0,
        'max_val_sent': 0,
        'avg_val_sent': 0,
        'avg_min_between_sent_tnx': 0
    }

    if 'sent' in sample_df_grouped.groups:
        sent_df = sample_df_grouped.get_group('sent')
        sent_df['gas_fee_eth'] = Web3.from_wei(
            sent_df['gasPrice'] * sent_df['gasUsed'], 'ether')
        sent_stats['avg_gas_fee'] = sent_df['gas_fee_eth'].mean()
        sent_stats['total_ether_sent'] = sent_df['eth_value'].sum()
        sent_stats['unique_sent_to_addresses'] = sent_df['to'].nunique()
        sent_stats['sent_tnx'] = len(sent_df)
        sent_stats['min_val_sent'] = sent_df['eth_value'].min()
        sent_stats['max_val_sent'] = sent_df['eth_value'].max()
        sent_stats['avg_val_sent'] = sent_df['eth_value'].mean()
        sent_stats['avg_min_between_sent_tnx'] = sent_df['timeStamp'].diff(
        ).sum().total_seconds() / 60 / len(sent_df)

    # Initialize statistics for received transactions
    received_stats = {
        'received_tnx': 0,
        'min_value_received': 0,
        'max_value_received': 0,
        'avg_value_received': 0,
        'total_ether_received': 0,
        'unique_received_from_addresses': 0,
        'avg_min_between_received_tnx': 0
    }

    if 'received' in sample_df_grouped.groups:
        received_df = sample_df_grouped.get_group('received')

        received_stats['received_tnx'] = len(received_df)
        received_stats['min_value_received'] = received_df['eth_value'].min()
        received_stats['max_value_received'] = received_df['eth_value'].max()
        received_stats['avg_value_received'] = received_df['eth_value'].mean()
        received_stats['total_ether_received'] = received_df['eth_value'].sum()
        received_stats['unique_received_from_addresses'] = received_df['from'].nunique()
        received_stats['avg_min_between_received_tnx'] = received_df['timeStamp'].diff(
        ).sum().total_seconds() / 60 / len(received_df)

    # Compile overall statistics
    overall_stats = {
        'address': address,
        'avg_sent_time': sent_stats['avg_min_between_sent_tnx'],
        'avg_received_time': received_stats['avg_min_between_received_tnx'],
        'time_difference_mins': (sample_df['timeStamp'].max() - sample_df['timeStamp'].min()).total_seconds() / 60,
        'sent': sent_stats['sent_tnx'],
        'received': received_stats['received_tnx'],
        'errors': len(sample_df[sample_df['isError'] != 0]),
        'unique_received_addresses': received_stats['unique_received_from_addresses'],
        'unique_sent_addresses': sent_stats['unique_sent_to_addresses'],
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
   
    return pd.DataFrame([overall_stats])
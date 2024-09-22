#!/usr/bin/env python3
""" 102-log_stats.py """

from pymongo import MongoClient


def print_log_stats():
    """
    Improves 12-log_stats.py by adding most present IPs
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    # Total logs
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    # HTTP methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    # Status check
    status_check = nginx_collection.count_documents(
            {"method": "GET", "path": "/status"})
    print(f"{status_check} status check")

    # Top 10 IPs
    print("IPs:")
    pipeline = [
        {
            "$group": {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        },
        {
            "$limit": 10
        }
    ]
    top_ips = nginx_collection.aggregate(pipeline)

    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    print_log_stats()

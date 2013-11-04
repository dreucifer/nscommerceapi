#!/usr/bin/env python
"""
Take in a FedEx tracking number list as csv and iterate over it, uploading
tracking numbers with the NsCommerceApi
"""

from nscommerceapi import NsCommerceApi
from orders import read_order, update_order
from csv import reader, excel_tab


def parse_usps(label, headers):
    """Action to apply to each label, mainly add the USPS bit to the order that
    matches (by name)
    """
    reference = label[headers.index("Reference Number")]
    label_num = label[headers.index("Label #")]
    name = label[headers.index("Delivery Name")]
    if reference is not " " or reference is not None:
        print update_order(CLIENT, order=[reference], tracking=[label_num])
    print " - ".join([reference, label_num, name])


def usps_numbers(filename="Labels.csv"):
    """@todo: Docstring for usps_numbers.
    """
    with open(filename, "rU") as label_file:
        label_file.readline()
        headers = label_file.readline().split(", ")
        labels = reader(label_file, dialect=excel_tab, delimiter=",")
        for label in labels:
            parse_usps(label, headers)


def parse_fedex(line):
    """@todo: Docstring for parse_fedex.
    """
    number = line[0]
    reference = line[32]
    name = line[10]
    if reference is not None:
        print update_order(CLIENT, order=[reference], tracking=[number])
    print " - ".join([reference, number, name])


def fedex_numbers(filename="tracking_nums.csv"):
    """@todo: Docstring for fedex_numbers.
    """
    with open(filename, "rU") as fedex_file:
        numbers = reader(fedex_file, dialect=excel_tab, delimiter=",")
        for number in numbers:
            parse_fedex(number)


def main():
    """@todo: Docstring for main.
    :returns: @todo

    """

    fedex_numbers()
    usps_numbers()

if __name__ == "__main__":
    API = NsCommerceApi()
    CLIENT = API.client

    main()

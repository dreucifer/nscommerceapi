#!/usr/bin/env python
"""
Take in a FedEx tracking number list as csv and iterate over it, uploading
tracking numbers with the NsCommerceApi
"""

from orders import Orders
from csv import reader, excel_tab
from urllib2 import URLError


def parse_usps(line, headers):
    """Action to apply to each label, mainly add the USPS bit to the order that
    matches (by name)
    """
    label_num = line[headers.index("Label #")]
    name = line[headers.index("Delivery Name")]
    reference = line[headers.index("Reference Number")]
    if reference == '' or reference == ' ':
        reference = ''
#       reference = raw_input(
#           "Please Enter a reference number for %s's order: " % name)
    print " - ".join([(reference or 'null'), label_num, name])
    return dict(order=[reference], tracking=[label_num])


def usps_numbers(filename="Labels.csv"):
    """@todo: Docstring for usps_numbers."""
    with open(filename, "rU") as label_file:
        label_file.readline()
        headers = label_file.readline().split(", ")
        labels = reader(label_file, dialect=excel_tab, delimiter=",")
        for label in labels:
            yield parse_usps(label, headers)


def parse_fedex(line):
    """@todo: Docstring for parse_fedex."""
    number = line[0]
    name = line[10]
    reference = [x for x in line[32:34] if x != 'null']
    if len(reference) > 0:
        reference = reference[0]
    if not reference or reference == 'null':
        reference = ''
#       reference = raw_input(
#           "Please Enter a reference number for %s's order: " % name)
    print " - ".join([reference, number, name])
    return dict(order=[reference], tracking=[number])


def fedex_numbers(filename="FedExHistoryExport.csv"):
    """@todo: Docstring for fedex_numbers.
    """
    with open(filename, "rU") as fedex_file:
        numbers = reader(fedex_file, dialect=excel_tab, delimiter=",")
        for number in numbers:
            if not number:
                continue
            yield parse_fedex(number)


def tracking_update(tracking, update):
    for order in tracking:
        while True:
            try:
                print update(**order)
            except URLError:
                print 'error!'
                continue
            break


def main():
    """@todo: Docstring for main.
    :returns: @todo

    """

    update = ORDERS.update

    print tracking_update(fedex_numbers(), update)
    print tracking_update(usps_numbers(), update)


if __name__ == "__main__":
    ORDERS = Orders()

    main()

from subprocess import *
import gzip
import string
import os
import time
import ApplePythonReporter

class ApplePythonReport:
    vendorId = YOUR_VENDOR_ID
    userId = 'YOUR_ITUNES_CONNECT_ACCOUNT_MAIL'
    password = 'ITUNES_CONNECT_PASSWORD'
    account = 'ACCOUNT_ID'
    mode = 'Robot.XML'
    dateType = 'Daily'
    eventIndex = 1
    activeSubscriberIndex = 16
    quantityIndex = 25

    subscribers = 0
    cancellations = 0
    activeSubscribers = 0
    maxAttempts = 5

    subscriptionReport = None
    subscriptionEventReport = None

    def __init__(self, reportDate):
        self.DownloadSubscriptionEventReport(reportDate)
        self.DownloadSubscriptionReport(reportDate)
        self.FetchSubscriptionEventData(reportDate)
        self.FetchSubscriptionData(reportDate)

    def DownloadSubscriptionEventReport(self, date):
        print 'Downloading Apple Financial Report for Subscriptions (' + date + ')..'
        credentials = (self.userId, self.password, self.account, self.mode)
        command = 'Sales.getReport, {0},SubscriptionEvent,Summary,{1},{2}'.format(self.vendorId, self.dateType, date)
        self.subscriptionEventReport = ApplePythonReporter.output_result(ApplePythonReporter.post_request(ApplePythonReporter.ENDPOINT_SALES, credentials, command))

    def DownloadSubscriptionReport(self, date):
        print 'Downloading Apple Financial Report for Active Users (' + date + ')..'
        credentials = (self.userId, self.password, self.account, self.mode)
        command = 'Sales.getReport, {0},Subscription,Summary,{1},{2}'.format(self.vendorId, self.dateType, date)
        self.subscriptionReport = ApplePythonReporter.output_result(ApplePythonReporter.post_request(ApplePythonReporter.ENDPOINT_SALES, credentials, command))

    #Uncompress and extract needed values (cancellations and new subscribers)
    def FetchSubscriptionEventData(self, date):
        if self.subscriptionEventReport is not None:
            print 'Fetching SubscriptionEvents..'
            text = self.subscriptionEventReport.splitlines()
            for row in text[1:]:
                line = string.split(row, '\t')
                # print line[self.eventIndex].__str__()
                if line[0].__str__().endswith(date[-2:]):
                    if line[self.eventIndex] == 'Cancel':
                        self.cancellations += int(line[self.quantityIndex])
                    if line[self.eventIndex] == 'Subscribe':
                        self.subscribers += int(line[self.quantityIndex])
        else:
            print 'SubscriptionEvent: There were no sales for the date specified'

    # Uncompress and extract needed values (active users)
    def FetchSubscriptionData(self, date):
        if self.subscriptionReport is not None:
            print 'Fetching Subscriptions..'
            text = self.subscriptionReport.splitlines()
            for row in text[1:]:
                line = string.split(row, '\t')
                self.activeSubscribers += int(line[self.activeSubscriberIndex])
        else:
            print 'Subscription: There were no sales for the date specified'
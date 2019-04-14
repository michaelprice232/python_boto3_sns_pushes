"""
Script to send a message to an SNS topic via the boto3 SDK
Lists all the SNS topics in the configured AWS region and requests the user to select a topic & message to send
"""

import boto3

# Create SNS client
sns = boto3.client('sns')

# Retrieve the AWS region which is currently being used. We are only listing SNS topics in the current region
my_session = boto3.session.Session()
my_region = my_session.region_name


def send_message(topic, msg):
    """Send a message to an SNS topic"""

    response = sns.publish(
        TopicArn=topic,
        Message=msg,
        Subject='Info: message from admin',
    )

    return response


def list_topics():
    """List all of the SNS topics in the region. Return a map with the keys as integers, topic ARNs as values"""

    # Retrieve all the SNS topics in the region
    response = sns.list_topics()

    # Empty dict to store structure to return to the user. Key is an integer, value is the topic arn
    topics_list = {}

    # Keep track of the number of topics, so it can be used as the key in in the dict
    item_number = 1
    # Loop through, the raw SNS topics and append to map in agreed format
    for topics in response['Topics']:
        topics_list[item_number] = topics['TopicArn']
        item_number += 1

    return topics_list


# List the SNS topics in the region
print("Listing the SNS topics in the configured AWS region (" + my_region + "):\n")
sns_topics_in_region = list_topics()
for identifier, topic_arn in sns_topics_in_region.items():
    print(str(identifier) + ': ' + str(topic_arn))

# Request the user to select which topic to send to
requested_topic_input = input("\nWhich SNS topic do you want to post to (enter number): ")

# Check that the input is not empty
if requested_topic_input:
    # Check that an integer value has been entered
    if requested_topic_input.isdigit():
        topic_selected = sns_topics_in_region[int(requested_topic_input)]

        # Request the user to input the message they want to send to the SNS topic
        message_to_send = input("Message to send to SNS topic (" + topic_selected + "): ")
        print("Sending '" + message_to_send + "' to " + topic_selected)

        # Send the message to topic, print out the response the received from the API cal
        print("\nSNS response: ", "\n", send_message(topic_selected, message_to_send))

    else:
        print("Error: you must enter an integer value")
        exit(1)
else:
    print("Error: you must select a topic (by entering the integer value")
    exit(1)

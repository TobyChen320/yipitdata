## yipitdata

# Download from bucket

If you wish to download your own copy of the files in the bucket. Just enter this cmd into your terminal. (This only works if you have aws-cli).

[aws-cli installation](https://aws.amazon.com/cli/)

'''
aws s3 cp --recursive s3://yipit-oscars-data "folder_name_to_download_to"
'''

# Running the code
I made running this code as simple as possible. All you have to do is run the main file. There are certain libraries you would need to run this. However a majority of them are standard libraries that anyone that works with data should have. If you don't have the libraries:
'''
pip install pandas
pip install numpy
pip install regex
pip install requests
'''
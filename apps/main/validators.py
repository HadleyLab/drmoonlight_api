from rest_framework import serializers


def validate_file_size(temp_file):
    if temp_file.size > 1024 * 1024 * 10:  # 10 megabytes
        raise serializers.ValidationError('File is too big (> 10Mb)')

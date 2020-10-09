import ipaddress


class RequestedIPsValidator:

    @staticmethod
    def validate_ip_address_range(ip_range):
        """
        :param str ip_range:
        """
        def raise_err(message):
            raise ValueError('{}. {} is not a valid IP Address range. Valid example: 10.0.0.1-10'.format(message, ip_range))

        # 1. validate basic structure
        address_and_range = ip_range.split('-')
        if not len(address_and_range) == 2:
            raise_err('Missing delimiter')

        ip = unicode(address_and_range[0])

        # 2. validate that the IP address part of the range has a valid IP address
        RequestedIPsValidator.validate_ip_address(ip)

        # 3. validate the 'length' part of the range is a valid integer
        range_length = 0
        try:
            range_length = int(address_and_range[1])
        except:
            raise_err('The range length is not a valid integer')

        # 4. validate max length for range 'length'
        if range_length > 253:
            raise raise_err('The range max length is 253')

        # 5. validate that all IPs in the range are legal
        ip_range_start = ipaddress.ip_address(ip)
        ip_range_end = ip_range_start + range_length
        network = ipaddress.ip_network(ip[:ip.rfind('.')] + u'.0/24')
        if ip_range_end not in network:
            raise_err('Requested range is illegal. All IPs in the range should be in the same network')

    @staticmethod
    def validate_ip_address(ip):
        """
        :param str ip:
        """
        # if ip address is not valid the following line will raise an exception
        ipaddress.ip_address(unicode(ip))

    @staticmethod
    def is_range(ip):
        """
        :param str ip:
        :rtype: bool
        """
        try:
            RequestedIPsValidator.validate_ip_address_range(ip)
            return True
        except:
            return False
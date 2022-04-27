from solution import Solution
import json
import copy


def main():
    solution = Solution()

    # Problem 1
    # Sample input output test
    print('\n\n' + '.'*20 + 'Problem 1' + '.'*20)
    if solution.special_bits(L=1, R=10, k=1) != 1:
        print("incorrect!")
    if solution.special_bits(L=1, R=10, k=2) != 3:
        print("incorrect!")
    if solution.special_bits(L=1, R=10, k=3) != 7:
        print("incorrect!")
    if solution.special_bits(L=1, R=10, k=4) != -1:
        print("incorrect!")

    # Problem 2
    print('\n\n' + '.'*20 + 'Problem 2' + '.'*20)
    if solution.toggle_string("ANkit") != "anKIT":
        print("incorrect!")
    if solution.toggle_string("abCDe") != "ABcdE":
        print("incorrect!")

    # Problem 3
    print('\n\n' + '.'*20 + 'Problem 3' + '.'*20)
    message = {
        "name": "John",
        "msg": "Beautiful is better than ugly."
        }
    send_data = solution.send_message(copy.copy(message))
    recv_data = solution.recv_message(send_data)
    if message == recv_data:
        print(message) 
        print(send_data)
        print(recv_data)

    
    # Problem 4
    print('\n\n' + '.'*20 + 'Problem 4' + '.'*20)
    cert, cipher, message_from_server = solution.client('localhost', 1060, cafile = 'ssu.crt')
    print(json.dumps(cert, indent=4, sort_keys=True))
    print("Cipher chosen for the connection...", cipher)
    print('Message from server................', message_from_server)
    

if __name__ == '__main__':
    main()
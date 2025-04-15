from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from .models import CipherTool, Category
import hashlib
import base64
import urllib.parse
import html
import binascii
import re

class HomeView(TemplateView):
    template_name = 'tools/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tools'] = CipherTool.objects.all()[:6]  # Show first 6 tools on homepage
        return context

class AboutView(TemplateView):
    template_name = 'tools/about.html'

class ToolsListView(ListView):
    model = CipherTool
    template_name = 'tools/tools_list.html'
    context_object_name = 'tools'
    
    def get_queryset(self):
        queryset = CipherTool.objects.all()
        
        # Filter by category if provided
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        # Filter by search query if provided
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        
        # Add search query to context
        context['search_query'] = self.request.GET.get('q', '')
        
        # Add selected category to context
        category_slug = self.request.GET.get('category')
        if category_slug:
            context['selected_category'] = get_object_or_404(Category, slug=category_slug)
        
        return context

class ToolDetailView(DetailView):
    model = CipherTool
    template_name = 'tools/tool_detail.html'
    context_object_name = 'tool'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_tools'] = CipherTool.objects.exclude(id=self.object.id)[:3]
        context['categories'] = Category.objects.all()
        return context

# Utility class for encoding/decoding operations
class CipherHandler:
    @staticmethod
    def md5_encode(text):
        return hashlib.md5(text.encode()).hexdigest()
    
    @staticmethod
    def sha1_encode(text):
        return hashlib.sha1(text.encode()).hexdigest()
    
    @staticmethod
    def sha256_encode(text):
        return hashlib.sha256(text.encode()).hexdigest()
    
    @staticmethod
    def base64_encode(text):
        return base64.b64encode(text.encode()).decode()
    
    @staticmethod
    def base64_decode(text):
        try:
            return base64.b64decode(text.encode()).decode()
        except:
            return "Invalid Base64 input"
    
    @staticmethod
    def url_encode(text):
        return urllib.parse.quote(text)
    
    @staticmethod
    def url_decode(text):
        try:
            return urllib.parse.unquote(text)
        except:
            return "Invalid URL-encoded input"
    
    @staticmethod
    def html_encode(text):
        return html.escape(text)
    
    @staticmethod
    def html_decode(text):
        try:
            return html.unescape(text)
        except:
            return "Invalid HTML-encoded input"
    
    @staticmethod
    def binary_encode(text):
        return ' '.join(format(ord(c), '08b') for c in text)
    
    @staticmethod
    def binary_decode(text):
        try:
            binary_values = text.split()
            return ''.join(chr(int(binary, 2)) for binary in binary_values)
        except:
            return "Invalid binary input"
    
    @staticmethod
    def hex_encode(text):
        return binascii.hexlify(text.encode()).decode()
    
    @staticmethod
    def hex_decode(text):
        try:
            return binascii.unhexlify(text.strip()).decode()
        except:
            return "Invalid hexadecimal input"
    
    @staticmethod
    def morse_encode(text):
        morse_code_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
            'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', 
            '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', 
            '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..', 
            "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-', 
            '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', 
            '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.'
        }
        
        encoded_text = []
        for char in text.upper():
            if char == ' ':
                encoded_text.append('/')
            elif char in morse_code_dict:
                encoded_text.append(morse_code_dict[char])
        
        return ' '.join(encoded_text)
    
    @staticmethod
    def morse_decode(text):
        morse_code_dict = {
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', 
            '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', 
            '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R', 
            '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', 
            '-.--': 'Y', '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', 
            '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7', 
            '---..': '8', '----.': '9', '.-.-.-': '.', '--..--': ',', '..--..': '?', 
            '.----.': "'", '-.-.--': '!', '-..-.': '/', '-.--.': '(', '-.--.-': ')', 
            '.-...': '&', '---...': ':', '-.-.-.': ';', '-...-': '=', '.-.-.': '+', 
            '-....-': '-', '..--.-': '_', '.-..-.': '"', '...-..-': '$', '.--.-.': '@'
        }
        
        decoded_text = []
        # Split by spaces
        words = text.split(' / ')
        for word in words:
            chars = word.split()
            for char in chars:
                if char in morse_code_dict:
                    decoded_text.append(morse_code_dict[char])
            decoded_text.append(' ')
        
        return ''.join(decoded_text).strip()
    
    @staticmethod
    def caesar_cipher_encode(text, shift=3):
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = ord('a') if char.islower() else ord('A')
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result
    
    @staticmethod
    def caesar_cipher_decode(text, shift=3):
        return CipherHandler.caesar_cipher_encode(text, 26 - shift)
    
    @staticmethod
    def atbash_encode(text):
        result = ""
        for char in text:
            if char.isalpha():
                if char.islower():
                    # a -> z, b -> y, etc.
                    result += chr(219 - ord(char))  # 219 = ord('a') + ord('z')
                else:
                    # A -> Z, B -> Y, etc.
                    result += chr(155 - ord(char))  # 155 = ord('A') + ord('Z')
            else:
                result += char
        return result
    
    @staticmethod
    def atbash_decode(text):
        # Atbash is its own inverse
        return CipherHandler.atbash_encode(text)
    
    @staticmethod
    def rot13_encode(text):
        return CipherHandler.caesar_cipher_encode(text, 13)
    
    @staticmethod
    def rot13_decode(text):
        return CipherHandler.caesar_cipher_encode(text, 13)  # ROT13 is its own inverse
    
    @staticmethod
    def sha384_encode(text):
        return hashlib.sha384(text.encode()).hexdigest()
    
    @staticmethod
    def sha512_encode(text):
        return hashlib.sha512(text.encode()).hexdigest()
    
    @staticmethod
    def base32_encode(text):
        return base64.b32encode(text.encode()).decode()
    
    @staticmethod
    def base32_decode(text):
        try:
            return base64.b32decode(text.encode()).decode()
        except:
            return "Invalid Base32 input"
    
    @staticmethod
    def octal_encode(text):
        return ' '.join(format(ord(c), '03o') for c in text)
    
    @staticmethod
    def octal_decode(text):
        try:
            octal_values = text.split()
            return ''.join(chr(int(octal, 8)) for octal in octal_values)
        except:
            return "Invalid octal input"
    
    @staticmethod
    def decimal_encode(text):
        return ' '.join(str(ord(c)) for c in text)
    
    @staticmethod
    def decimal_decode(text):
        try:
            decimal_values = text.split()
            return ''.join(chr(int(decimal)) for decimal in decimal_values)
        except:
            return "Invalid decimal input"
    
    @staticmethod
    def vigenere_encode(text, key):
        result = ""
        key = key.upper()
        key_length = len(key)
        key_as_int = [ord(k) - ord('A') for k in key]
        
        for i, char in enumerate(text):
            if char.isalpha():
                # Determine the shift amount from the key
                key_index = i % key_length
                key_shift = key_as_int[key_index]
                
                # Apply the shift
                if char.isupper():
                    result += chr((ord(char) - ord('A') + key_shift) % 26 + ord('A'))
                else:
                    result += chr((ord(char) - ord('a') + key_shift) % 26 + ord('a'))
            else:
                result += char
                
        return result
    
    @staticmethod
    def vigenere_decode(text, key):
        result = ""
        key = key.upper()
        key_length = len(key)
        key_as_int = [ord(k) - ord('A') for k in key]
        
        for i, char in enumerate(text):
            if char.isalpha():
                # Determine the shift amount from the key
                key_index = i % key_length
                key_shift = key_as_int[key_index]
                
                # Apply the reverse shift
                if char.isupper():
                    result += chr((ord(char) - ord('A') - key_shift) % 26 + ord('A'))
                else:
                    result += chr((ord(char) - ord('a') - key_shift) % 26 + ord('a'))
            else:
                result += char
                
        return result
    
    @staticmethod
    def railfence_encode(text, rails):
        if rails < 2:
            return text
            
        # Create the rail fence pattern
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1  # 1 for going down, -1 for going up
        
        for char in text:
            fence[rail].append(char)
            rail += direction
            
            # Change direction when we reach the top or bottom rail
            if rail == 0 or rail == rails - 1:
                direction = -direction
                
        # Read off the fence
        result = ''.join([''.join(rail) for rail in fence])
        return result
    
    @staticmethod
    def railfence_decode(text, rails):
        if rails < 2 or not text:
            return text
            
        # Create the fence pattern
        fence = [[''] * len(text) for _ in range(rails)]
        
        # Mark the fence pattern with 'x' to know positions
        rail = 0
        direction = 1
        for i in range(len(text)):
            fence[rail][i] = 'x'
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        # Fill the fence with the encoded text
        index = 0
        for i in range(rails):
            for j in range(len(text)):
                if fence[i][j] == 'x' and index < len(text):
                    fence[i][j] = text[index]
                    index += 1
        
        # Read off the fence in zigzag order
        result = ''
        rail = 0
        direction = 1
        for i in range(len(text)):
            result += fence[rail][i]
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction = -direction
                
        return result
    
    @staticmethod
    def rot47_encode(text):
        result = ""
        for char in text:
            # Check if the character is in the range of printable ASCII
            if 33 <= ord(char) <= 126:
                # Apply ROT47 transformation (33 to 126, with shift of 47)
                shifted = ord(char) + 47
                if shifted > 126:
                    shifted = shifted - 94  # wrap around (126-33+1 = 94 range)
                result += chr(shifted)
            else:
                result += char
        return result
    
    @staticmethod
    def rot47_decode(text):
        result = ""
        for char in text:
            # Check if the character is in the range of printable ASCII
            if 33 <= ord(char) <= 126:
                # Apply reverse ROT47 transformation
                shifted = ord(char) - 47
                if shifted < 33:
                    shifted = shifted + 94  # wrap around
                result += chr(shifted)
            else:
                result += char
        return result
    
    @staticmethod
    def base85_encode(text):
        try:
            return base64.b85encode(text.encode()).decode()
        except:
            return "Error encoding Base85"
    
    @staticmethod
    def base85_decode(text):
        try:
            return base64.b85decode(text.encode()).decode()
        except:
            return "Invalid Base85 input"
    
    @staticmethod
    def affine_encode(text, a=5, b=8):
        result = ""
        # Ensure a is coprime with 26 (alphabet size)
        if a % 2 == 0 or a % 13 == 0:
            return "Parameter 'a' must be coprime with 26"
            
        for char in text:
            if char.isalpha():
                # Convert to 0-25
                if char.isupper():
                    # E(x) = (ax + b) mod 26
                    x = ord(char) - ord('A')
                    # Apply affine transformation
                    code = (a * x + b) % 26
                    result += chr(code + ord('A'))
                else:
                    x = ord(char) - ord('a')
                    code = (a * x + b) % 26
                    result += chr(code + ord('a'))
            else:
                result += char
        return result
    
    @staticmethod
    def affine_decode(text, a=5, b=8):
        result = ""
        # Calculate modular multiplicative inverse of a
        a_inv = -1
        for i in range(1, 26):
            if (a * i) % 26 == 1:
                a_inv = i
                break
                
        if a_inv == -1:
            return "Cannot decrypt: parameter 'a' has no modular inverse"
            
        for char in text:
            if char.isalpha():
                if char.isupper():
                    # D(y) = a^-1 * (y - b) mod 26
                    y = ord(char) - ord('A')
                    # Apply affine decryption
                    code = (a_inv * (y - b + 26)) % 26
                    result += chr(code + ord('A'))
                else:
                    y = ord(char) - ord('a')
                    code = (a_inv * (y - b + 26)) % 26
                    result += chr(code + ord('a'))
            else:
                result += char
        return result
    
    @staticmethod
    def bacon_encode(text):
        # Francis Bacon's cipher (A=00000, B=00001, etc.)
        bacon_dict = {
            'A': 'aaaaa', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa',
            'F': 'aabab', 'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'J': 'abaaa', 
            'K': 'abaab', 'L': 'ababa', 'M': 'ababb', 'N': 'abbaa', 'O': 'abbab',
            'P': 'abbba', 'Q': 'abbbb', 'R': 'baaaa', 'S': 'baaab', 'T': 'baaba',
            'U': 'baabb', 'V': 'baabb', 'W': 'babaa', 'X': 'babab', 'Y': 'babba', 
            'Z': 'babbb'
        }
        
        result = []
        for char in text.upper():
            if char.isalpha():
                result.append(bacon_dict[char])
            else:
                result.append(char)
                
        return ' '.join(result)
    
    @staticmethod
    def bacon_decode(text):
        # Francis Bacon's cipher (inverse)
        bacon_dict = {
            'aaaaa': 'A', 'aaaab': 'B', 'aaaba': 'C', 'aaabb': 'D', 'aabaa': 'E',
            'aabab': 'F', 'aabba': 'G', 'aabbb': 'H', 'abaaa': 'I/J', 'abaab': 'K',
            'ababa': 'L', 'ababb': 'M', 'abbaa': 'N', 'abbab': 'O', 'abbba': 'P',
            'abbbb': 'Q', 'baaaa': 'R', 'baaab': 'S', 'baaba': 'T', 'baabb': 'U/V',
            'babaa': 'W', 'babab': 'X', 'babba': 'Y', 'babbb': 'Z'
        }
        
        result = ""
        # Split by spaces and process each bacon code
        parts = text.lower().split()
        for part in parts:
            # Check if it's a valid bacon code
            if part in bacon_dict:
                result += bacon_dict[part]
            else:
                # Try to replace 'a's and 'b's with different symbols
                processed = part
                for char in set(part) - {'a', 'b'}:
                    if len(set(part)) == 3 and char in part:
                        # Replace third character with space
                        processed = processed.replace(char, ' ')
                    
                # Split by spaces if any
                if ' ' in processed:
                    for subpart in processed.split():
                        if subpart in bacon_dict:
                            result += bacon_dict[subpart]
                        else:
                            result += subpart
                else:
                    # Keep original character if not a bacon code
                    result += part
                
        return result
    
    @staticmethod
    def polybius_encode(text):
        # Standard 5x5 Polybius square (I/J combined)
        square = [
            ['A', 'B', 'C', 'D', 'E'],
            ['F', 'G', 'H', 'I/J', 'K'],
            ['L', 'M', 'N', 'O', 'P'],
            ['Q', 'R', 'S', 'T', 'U'],
            ['V', 'W', 'X', 'Y', 'Z']
        ]
        
        result = ""
        for char in text.upper():
            if char.isalpha():
                # Replace J with I
                if char == 'J':
                    char = 'I'
                
                # Find coordinates in the square
                for row_idx, row in enumerate(square):
                    for col_idx, cell in enumerate(row):
                        if char in cell:
                            # Polybius coordinates are 1-based
                            result += f"{row_idx+1}{col_idx+1} "
                            break
            else:
                result += char
                
        return result.strip()
    
    @staticmethod
    def polybius_decode(text):
        # Standard 5x5 Polybius square (I/J combined)
        square = [
            ['A', 'B', 'C', 'D', 'E'],
            ['F', 'G', 'H', 'I/J', 'K'],
            ['L', 'M', 'N', 'O', 'P'],
            ['Q', 'R', 'S', 'T', 'U'],
            ['V', 'W', 'X', 'Y', 'Z']
        ]
        
        result = ""
        digits = ''.join(filter(str.isdigit, text))
        
        # Process digit pairs
        for i in range(0, len(digits), 2):
            if i+1 < len(digits):
                row = int(digits[i]) - 1
                col = int(digits[i+1]) - 1
                
                if 0 <= row < 5 and 0 <= col < 5:
                    result += square[row][col].split('/')[0]  # Get first char if there's a '/'
                else:
                    result += f"?({digits[i]}{digits[i+1]})"
        
        return result

# AJAX views for handling encoding/decoding operations
def process_text(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        text = request.POST.get('text', '')
        operation = request.POST.get('operation', '')
        tool_type = request.POST.get('tool_type', '')
        
        handler = CipherHandler()
        result = ""
        
        if tool_type == 'md5':
            if operation == 'encode':
                result = handler.md5_encode(text)
        elif tool_type == 'sha1':
            if operation == 'encode':
                result = handler.sha1_encode(text)
        elif tool_type == 'sha256':
            if operation == 'encode':
                result = handler.sha256_encode(text)
        elif tool_type == 'base64':
            if operation == 'encode':
                result = handler.base64_encode(text)
            else:
                result = handler.base64_decode(text)
        elif tool_type == 'url':
            if operation == 'encode':
                result = handler.url_encode(text)
            else:
                result = handler.url_decode(text)
        elif tool_type == 'html':
            if operation == 'encode':
                result = handler.html_encode(text)
            else:
                result = handler.html_decode(text)
        elif tool_type == 'binary':
            if operation == 'encode':
                result = handler.binary_encode(text)
            else:
                result = handler.binary_decode(text)
        elif tool_type == 'hex':
            if operation == 'encode':
                result = handler.hex_encode(text)
            else:
                result = handler.hex_decode(text)
        elif tool_type == 'morse':
            if operation == 'encode':
                result = handler.morse_encode(text)
            else:
                result = handler.morse_decode(text)
        elif tool_type == 'caesar':
            try:
                shift = int(request.POST.get('shift', '3'))
                if shift < 1:
                    shift = 1
                elif shift > 25:
                    shift = 25
            except ValueError:
                shift = 3
                
            if operation == 'encode':
                result = handler.caesar_cipher_encode(text, shift)
            else:
                result = handler.caesar_cipher_decode(text, shift)
        elif tool_type == 'atbash':
            if operation == 'encode':
                result = handler.atbash_encode(text)
            else:
                result = handler.atbash_decode(text)
        elif tool_type == 'rot13':
            if operation == 'encode':
                result = handler.rot13_encode(text)
            else:
                result = handler.rot13_decode(text)
        elif tool_type == 'sha384':
            if operation == 'encode':
                result = handler.sha384_encode(text)
        elif tool_type == 'sha512':
            if operation == 'encode':
                result = handler.sha512_encode(text)
        elif tool_type == 'base32':
            if operation == 'encode':
                result = handler.base32_encode(text)
            else:
                result = handler.base32_decode(text)
        elif tool_type == 'octal':
            if operation == 'encode':
                result = handler.octal_encode(text)
            else:
                result = handler.octal_decode(text)
        elif tool_type == 'decimal':
            if operation == 'encode':
                result = handler.decimal_encode(text)
            else:
                result = handler.decimal_decode(text)
        elif tool_type == 'vigenere':
            key = request.POST.get('key', 'KEY')
            if not key.strip():
                key = 'KEY'
            if operation == 'encode':
                result = handler.vigenere_encode(text, key)
            else:
                result = handler.vigenere_decode(text, key)
        elif tool_type == 'railfence':
            try:
                rails = int(request.POST.get('rails', '3'))
                if rails < 2:
                    rails = 2
                elif rails > 10:
                    rails = 10
            except ValueError:
                rails = 3
                
            if operation == 'encode':
                result = handler.railfence_encode(text, rails)
            else:
                result = handler.railfence_decode(text, rails)
        elif tool_type == 'rot47':
            if operation == 'encode':
                result = handler.rot47_encode(text)
            else:
                result = handler.rot47_decode(text)
        elif tool_type == 'base85':
            if operation == 'encode':
                result = handler.base85_encode(text)
            else:
                result = handler.base85_decode(text)
        elif tool_type == 'affine':
            try:
                a = int(request.POST.get('a', '5'))
                b = int(request.POST.get('b', '8'))
            except ValueError:
                a, b = 5, 8
                
            if operation == 'encode':
                result = handler.affine_encode(text, a, b)
            else:
                result = handler.affine_decode(text, a, b)
        elif tool_type == 'bacon':
            if operation == 'encode':
                result = handler.bacon_encode(text)
            else:
                result = handler.bacon_decode(text)
        elif tool_type == 'polybius':
            if operation == 'encode':
                result = handler.polybius_encode(text)
            else:
                result = handler.polybius_decode(text)
        
        return JsonResponse({'result': result})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

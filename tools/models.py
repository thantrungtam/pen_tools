from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

class CipherTool(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    tool_type_choices = [
        ('encode', 'Encoder'),
        ('decode', 'Decoder'),
        ('both', 'Encoder/Decoder')
    ]
    tool_type = models.CharField(max_length=10, choices=tool_type_choices, default='both')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='tools')
    icon = models.CharField(max_length=50, default='fa-tools')  # Font Awesome icon class
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('tool_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['order', 'name']

def create_default_data():
    # Create categories if they don't exist
    encoders, _ = Category.objects.get_or_create(
        name="Encoders & Decoders",
        slug="encoders-decoders",
        defaults={'description': 'Tools for encoding and decoding data in various formats.'}
    )
    
    hash_functions, _ = Category.objects.get_or_create(
        name="Hash Functions",
        slug="hash-functions",
        defaults={'description': 'One-way hash functions for generating message digests.'}
    )
    
    classical, _ = Category.objects.get_or_create(
        name="Classical Ciphers",
        slug="classical-ciphers",
        defaults={'description': 'Historical encryption techniques used before modern cryptography.'}
    )
    
    utilities, _ = Category.objects.get_or_create(
        name="Text Utilities",
        slug="text-utilities",
        defaults={'description': 'Useful text transformation and analysis tools.'}
    )
    
    number_systems, _ = Category.objects.get_or_create(
        name="Number Systems",
        slug="number-systems", 
        defaults={'description': 'Tools for converting between different number bases and representations.'}
    )
    
    # Create tools if they don't exist
    
    # Base encoders
    CipherTool.objects.get_or_create(
        slug='base64',
        defaults={
            'name': 'Base64',
            'description': 'Encode or decode text using Base64 encoding.',
            'category': encoders,
            'tool_type': 'both',
            'icon': 'fa-exchange-alt'
        }
    )
    
    CipherTool.objects.get_or_create(
        slug='base32',
        defaults={
            'name': 'Base32',
            'description': 'Encode or decode text using Base32 encoding.',
            'category': encoders,
            'tool_type': 'both',
            'icon': 'fa-exchange-alt'
        }
    )
    
    CipherTool.objects.get_or_create(
        slug='hex',
        defaults={
            'name': 'Hex Encoder/Decoder',
            'description': 'Convert text to hexadecimal representation and back.',
            'category': encoders,
            'tool_type': 'both',
            'icon': 'fa-code'
        }
    )
    
    CipherTool.objects.get_or_create(
        slug='binary',
        defaults={
            'name': 'Binary Text Converter',
            'description': 'Convert text to binary representation and back.',
            'category': encoders,
            'tool_type': 'both',
            'icon': 'fa-binary'
        }
    )
    
    CipherTool.objects.get_or_create(
        slug='octal',
        defaults={
            'name': 'Octal Encoder/Decoder',
            'description': 'Convert text to octal representation and back.',
            'category': number_systems,
            'tool_type': 'both',
            'icon': 'fa-calculator'
        }
    )
    
    CipherTool.objects.get_or_create(
        slug='decimal',
        defaults={
            'name': 'Decimal (ASCII) Converter',
            'description': 'Convert text to decimal ASCII values and back.',
            'category': number_systems,
            'tool_type': 'both',
            'icon': 'fa-sort-numeric-up'
        }
    )
    
    # Hash functions
    CipherTool.objects.get_or_create(
        slug='md5',
        defaults={
            'name': 'MD5 Hash',
            'description': 'Generate MD5 hash of text input (one-way function).',
            'category': hash_functions,
            'tool_type': 'encode',
            'icon': 'fa-fingerprint'
        }
    )
    
    CipherTool.objects.get_or_create(
        slug='sha1',
        defaults={
            'name': 'SHA-1 Hash',
            'description': 'Generate SHA-1 hash of text input (one-way function).',
            'category': hash_functions,
            'tool_type': 'encode',
            'icon': 'fa-fingerprint'
        }
    )
    
    CipherTool.objects.get_or_create(
        slug='sha256',
        defaults={
            'name': 'SHA-256 Hash',
            'description': 'Generate SHA-256 hash of text input (one-way function).',
            'category': hash_functions,
            'tool_type': 'encode',
            'icon': 'fa-fingerprint'
        }
    )
    
    CipherTool.objects.get_or_create(
        slug='sha384',
        defaults={
            'name': 'SHA-384 Hash',
            'description': 'Generate SHA-384 hash of text input (one-way function).',
            'category': hash_functions,
            'tool_type': 'encode',
            'icon': 'fa-fingerprint'
        }
    )
    
    CipherTool.objects.get_or_create(
        slug='sha512',
        defaults={
            'name': 'SHA-512 Hash',
            'description': 'Generate SHA-512 hash of text input (one-way function).',
            'category': hash_functions,
            'tool_type': 'encode',
            'icon': 'fa-fingerprint'
        }
    )
    
    # Classical ciphers
    CipherTool.objects.get_or_create(
        slug='caesar',
        defaults={
            'name': 'Caesar Cipher',
            'description': 'Encrypt or decrypt text using the Caesar shift cipher.',
            'category': classical,
            'tool_type': 'both',
            'icon': 'fa-key'
        }
    )
    
    CipherTool.objects.get_or_create(
        slug='rot13',
        defaults={
            'name': 'ROT13 Cipher',
            'description': 'Encrypt or decrypt text using the ROT13 cipher (Caesar with shift 13).',
            'category': classical,
            'tool_type': 'both',
            'icon': 'fa-sync'
        }
    )
    
    CipherTool.objects.get_or_create(
        slug='atbash',
        defaults={
            'name': 'Atbash Cipher',
            'description': 'Encrypt or decrypt text using the Atbash cipher (alphabet reversal).',
            'category': classical,
            'tool_type': 'both',
            'icon': 'fa-sync-alt'
        }
    )
    
    CipherTool.objects.get_or_create(
        slug='vigenere',
        defaults={
            'name': 'Vigenère Cipher',
            'description': 'Encrypt or decrypt text using the Vigenère cipher with a keyword.',
            'category': classical,
            'tool_type': 'both',
            'icon': 'fa-key'
        }
    )
    
    CipherTool.objects.get_or_create(
        slug='railfence',
        defaults={
            'name': 'Rail Fence Cipher',
            'description': 'Encrypt or decrypt text using the Rail Fence (zigzag) transposition cipher.',
            'category': classical,
            'tool_type': 'both',
            'icon': 'fa-bars'
        }
    )
    
    # Text utilities
    CipherTool.objects.get_or_create(
        slug='morse',
        defaults={
            'name': 'Morse Code Translator',
            'description': 'Convert text to Morse code and back.',
            'category': utilities,
            'tool_type': 'both',
            'icon': 'fa-ellipsis-h'
        }
    )
    
    CipherTool.objects.get_or_create(
        slug='reverse',
        defaults={
            'name': 'Text Reverser',
            'description': 'Reverse the order of characters in text.',
            'category': utilities,
            'tool_type': 'both',
            'icon': 'fa-exchange-alt'
        }
    )
    
    CipherTool.objects.get_or_create(
        slug='url',
        defaults={
            'name': 'URL Encoder/Decoder',
            'description': 'Encode or decode text for use in URLs.',
            'category': utilities,
            'tool_type': 'both',
            'icon': 'fa-link'
        }
    )

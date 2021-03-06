#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    pygments.lexers.radare2
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Radare2 commandline output and Visual Mode.

"""

from pygments.lexer import RegexLexer, bygroups, include, words
from pygments.token import *

__all__ = ['Radare2Lexer']

class Radare2Lexer(RegexLexer):
    name = 'Radare2'
    aliases = ['r2', 'radare2']
    filenames = []

    tokens = {
        'root': [
            (r'^\$| -- ', Text, 'bashprompt'),
            (r'^ -- ', Text, 'bashprompt'),
            (r'^\[', Text, 'cmdprompt'),
            (r'^sys|usr', String, 'dmoutput'),
            (r'0[Xx]', String, 'addroutput'),
            (r'^[|\\/┌│└ ]', Keyword, 'pdoutput'),
            (r'^[^[]', Text, 'stroutput')
        ],

        'bashprompt': [
            (r'.+', Text, 'bashprompt'),
        ],

        'dmoutput': [
            (r'[0-9.]+(?:M|K)', Keyword),
            (r'0[Xx][0-9a-f]+', Number.Hex),
            (r'\bs\b', Text),
            (r'[rwx-]{4}', Operator),
            (r'[-*/_.;[\]]', Operator),
            (r' ', Text),
            (r'[A-Za-z0-9]+', Text)
        ],

        'pdoutput': [
            (r'[┌│└↑─<>]', Keyword),
            (r'[-+\*/&=]', Operator),
            (r'(\()(var)(\))', bygroups(Text, Number.Hex, Text)),
            (r'(\()(fcn)(\))', bygroups(Text, Operator, Text)),
            (r'local_[0-9a-z_]+', Keyword),
            (r'main', Text),

            (r'--', Text, 'stroutput'),
            (r'/|\||\\', Keyword),
            (r'[.,`][=-]+[<>]', Keyword),
            (r' ', Text),
            (r';$', Text),
            (r',', Operator),
            (r';', Comment, 'comment'),
            (r'\(\)', Text),

            (r'(\()(.+?)(\))', bygroups(Text, Keyword, Text)),
            (r'([A-Za-z]{3})(\.)([A-Za-z]{3})(\.)([\w.:]+)', bygroups(Keyword, Operator, Keyword, Operator, Text)),
            (r'([A-Za-z]{3})(\.)([\w.:]+)', bygroups(Keyword, Operator, Text)),
            (r'(0[Xx][0-9a-f]{8,})([ ]+)([0-9a-f]+\.?)([ ]+)', bygroups(String, Text, Text, Text)),
            (r'^(0[Xx][0-9a-f]{8,})([ ]+)(\.?[A-Za-z0-9]+)([ ]+)(0[Xx][0-9a-f]{8,})', bygroups(String, Text, Keyword, Text, Number.Hex)),

            include('stackops'),
            include('copyops'),
            include('arithmeticops'),
            include('logicops'),
            include('ipops'),
            include('otherops'),
            include('registers'),
            include('pseudocode'),
            (r'0[Xx][0-9a-f]+', Number.Hex),
            (r'[0-9a-f]', Number)
        ],

        'comment': [
            (r'.+$', Comment, '#pop')
        ],

        'cmdprompt': [
            (r'(0[xX][0-9a-f]+)(\])(>)(\s+)(\w+)?(.*)', bygroups(Number.Hex, Text, Operator, Text, Name.Function, Text)),
            (r'.+', Text)
        ],

        'addroutput': [
            (r'([0-9a-f]{8,})(\s+\d+\s\d+\s+)([0-9A-z\._]+)$', bygroups(String, Number.Hex, Text)),
            (r'([0-9a-f]{8,})(\s+\d+\s\d+)(\s*->)(\s\d*)(\s*[0-9A-z\._]+)$', bygroups(String, Number.Hex, Operator, Number.Hex, Text)),
            (r'([0-9a-f]{8,})(\s{2})([0-9A-z\s]+)(\s\s)(.{16})$', bygroups(String, Text, Number.Hex, Text, Text)),
            (r'([0-9a-f]+\s)(\d+\s)([0-9A-z/_ ]+)(]>)(.+)$', bygroups(String, Keyword, Operator, String, Text)),
            (r'([0-9a-f]+)(\s*)$', bygroups(String, Text))
        ],

        'stroutput': [
            (r'[A-Za-z%_)<>]+', Text),
            (r' ', Text),
            (r'(?:0[Xx])?[0-9a-f]+', Number.Hex),
            (r'[.:+/=-]', Operator),
            (r'[|]', Keyword),
        ],

        'pseudocode': [
            (words(('var', 'if', 'goto')), Number.Hex)
        ],

        'registers': [
            (words(('rsp', 'esp', 'spl', 'rbp', 'ebp', 'bpl', 'rax', 'eax', 'ah', 'al', 'rbx', 'ebx', 'bh', 'bl', 'rcx', 'ecx', 'cx', 'ch', 'cl', 'rdx', 'edx', 'dx', 'dh', 'dl', 'rdi', 'edi', 'dil', 'rsi', 'rip', 'esi', 'sil', 'r15', 'r14', 'r13', 'r12', 'r11', 'r10', 'r9', 'r9d', 'r8', 'r8d', 'rflags', 'fs:', 'gs:', 'cs:')),
            Keyword)
        ],

        'otherops': [
            (words(('in', 'byte', 'sbb', 'clc', 'nop', '.qword', 'qword', 'dword', 'local_', '[', 'h]', ']', '-', '+')),
            Text)
        ],

        'stackops': [
            (words(('push', 'pop'), prefix=r'\b', suffix=r'\b'),
            Keyword)
        ],

        'copyops': [
            (words(('mov', 'movzx', 'movsx', 'movabs', 'lea', 'rdtsc'), prefix=r'\b', suffix=r'\b'),
            Number)
        ],

        'logicops': [
            (words(('and', 'or', 'not', 'xor', 'cmp', 'word', 'test'), suffix=r'\b', prefix=r'\b'),
            String)
        ],

        'arithmeticops': [
            (words(('leave', 'add', 'sub', 'imul', 'mul', 'shl', 'shr', 'sar', 'sal'), suffix=r'\b', prefix=r'\b'),
            Operator)
        ],

        'ipops': [
            (words(('je', 'jmp', 'jne', 'jae', 'jbe', 'call', 'ret', 'syscall'), suffix=r'\b', prefix=r'\b'),
            Name.Function)
        ]
    }

class TexChar:
    def __init__(self, cmd, char, unicode):
        self.command = cmd
        self.char = char
        self.unicode = unicode


class TexCharSet:
    def __init__(self):
        self.charset = {}

    def add(self, cmd, char, unicode):
        self.charset[cmd] = TexChar(cmd, char, unicode)


TEX_CHARSET = TexCharSet()

# Greek small letter
TEX_CHARSET.add('alpha', 'α', 945)
TEX_CHARSET.add('beta', 'β', 946)
TEX_CHARSET.add('gamma', 'γ', 947)
TEX_CHARSET.add('delta', 'δ', 948)
TEX_CHARSET.add('epsilon', 'ε', 949)
TEX_CHARSET.add('zeta', 'ζ', 950)
TEX_CHARSET.add('eta', 'η', 951)
TEX_CHARSET.add('theta', 'θ', 952)
TEX_CHARSET.add('iota', 'ι', 953)
TEX_CHARSET.add('kappa', 'κ', 954)
TEX_CHARSET.add('lamda', 'λ', 955)
TEX_CHARSET.add('mu', 'μ', 956)
TEX_CHARSET.add('nu', 'ν', 957)
TEX_CHARSET.add('xi', 'ξ', 958)
TEX_CHARSET.add('omicron', 'ο', 959)
TEX_CHARSET.add('pi', 'π', 960)
TEX_CHARSET.add('rho', 'ρ', 961)
TEX_CHARSET.add('sigma', 'σ', 963)
TEX_CHARSET.add('tau', 'τ', 964)
TEX_CHARSET.add('upsilon', 'υ', 965)
TEX_CHARSET.add('phi', 'φ', 966)
TEX_CHARSET.add('chi', 'χ', 967)
TEX_CHARSET.add('psi', 'ψ', 968)
TEX_CHARSET.add('omega', 'ω', 969)

# Greek capital letter
TEX_CHARSET.add('Alpha', 'Α', 913)
TEX_CHARSET.add('Beta', 'Β', 914)
TEX_CHARSET.add('Gamma', 'Γ', 915)
TEX_CHARSET.add('Delta', 'Δ', 916)
TEX_CHARSET.add('Epsilon', 'Ε', 917)
TEX_CHARSET.add('Zeta', 'Ζ', 918)
TEX_CHARSET.add('Eta', 'Η', 919)
TEX_CHARSET.add('Theta', 'Θ', 920)
TEX_CHARSET.add('Iota', 'Ι', 921)
TEX_CHARSET.add('Kappa', 'Κ', 922)
TEX_CHARSET.add('Lamda', 'Λ', 923)
TEX_CHARSET.add('Mu', 'Μ', 924)
TEX_CHARSET.add('Nu', 'Ν', 925)
TEX_CHARSET.add('Xi', 'Ξ', 926)
TEX_CHARSET.add('Omicron', 'Ο', 927)
TEX_CHARSET.add('Pi', 'Π', 928)
TEX_CHARSET.add('Rho', 'Ρ', 929)
TEX_CHARSET.add('Sigma', 'Σ', 931)
TEX_CHARSET.add('Tau', 'Τ', 932)
TEX_CHARSET.add('Upsilon', 'Υ', 933)
TEX_CHARSET.add('Phi', 'Φ', 934)
TEX_CHARSET.add('Chi', 'Χ', 935)
TEX_CHARSET.add('Psi', 'Ψ', 936)
TEX_CHARSET.add('Omega', 'Ω', 937)

# Greek letter variant
TEX_CHARSET.add('varsigma', 'ς', 962)
TEX_CHARSET.add('varbeta', 'ϐ', 976)
TEX_CHARSET.add('vartheta', 'ϑ', 977)
TEX_CHARSET.add('varphi', 'ϕ', 981)
TEX_CHARSET.add('varpi', 'ϖ', 982)
TEX_CHARSET.add('stigma', 'Ϛ', 986)
TEX_CHARSET.add('digamma', 'Ϝ', 988)
TEX_CHARSET.add('koppa', 'Ϟ', 990)
TEX_CHARSET.add('sampi', 'Ϡ', 992)
TEX_CHARSET.add('varkappa', 'ϰ', 1008)
TEX_CHARSET.add('varrho', 'ϱ', 1009)
TEX_CHARSET.add('lunatesigma', 'ϲ', 1010)
from enum import Enum

class PayslipPriningLanguage(Enum):
    TYPE1 = ('EN', 'English')
    TYPE2 = ('FR', 'French')
    TYPE3 = ('HI', 'Hindi')

    @classmethod
    def choices(cls):
        return [(choice.value[0], choice.value[1]) for choice in cls]


class PayrollDeclarationsType(Enum):
    MRA = ('MRA', 'MRA')
    MNS = ('MNS', 'MNS')
    MRA_PACO = ('MRA_PACO', 'MRA (PACO)')

    @classmethod
    def choices(cls):
        return [(choice.value[0], choice.value[1]) for choice in cls]


class SalaryCalculationsPeriodChoices(Enum):
    MRA = ('monthly', 'Monthly')
    MNS = ('fortnightly', 'Fortnightly')
    MRA_PACO = ('weekly', 'Weekly')

    @classmethod
    def choices(cls):
        return [(choice.value[0], choice.value[1]) for choice in cls]


class EoyBonusOptions(Enum):
    TYPE1 = ('SEPARATE', 'Separate Payslip')
    TYPE2 = ('DEC', 'Included in Dec Salary')

    @classmethod
    def choices(cls):
        return [(choice.value[0], choice.value[1]) for choice in cls]


class BankSwiftCodes(Enum):
    MCB = ('MCBLMUMU', 'Mauritius Commercial Bank')
    SBM = ('STCBMUMU', 'State Bank of Mauritius')
    AFRASIA = ('AFBLMUMU', 'AfrAsia Bank')
    BANK_ONE = ('BKONMUMU', 'Bank One')
    MAUBANK = ('MUAUMUMU', 'MauBank')
    BCP = ('BMMMUMU', 'Banque des Mascareignes')
    ABSA = ('BARCMUMU', 'ABSA Bank Mauritius')

    @classmethod
    def choices(cls):
        return [(choice.value[0], choice.value[1]) for choice in cls]



class SupportedCurrencies(Enum):
    TYPE1 = ('MUR', 'MUR')
    TYPE2 = ('EUR', 'EUR')
    TYPE3 = ('USD', 'USD')
    TYPE4 = ('GBP', 'GBP')
    TYPE5 = ('JPY', 'JPY')

    @classmethod
    def choices(cls):
        return [(choice.value[0], choice.value[1]) for choice in cls]


class TimeUnits(Enum):
    TYPE1 = ('HOU', 'Hours')
    TYPE2 = ('MIN', 'Minutes')
    @classmethod
    def choices(cls):
        return [(choice.value[0], choice.value[1]) for choice in cls]


class OvertimeCalculationOptions(Enum):
    TYPE1 = ('AFTER_HOURS', 'After Normal Working Hours')
    TYPE2 = ('CUMUL_HOURS', 'Cumulative Hours(After and before Working hours also)')

    @classmethod
    def choices(cls):
        return [(choice.value[0], choice.value[1]) for choice in cls]

class GenderOptions(Enum):
    TYPE1 = ('MALE', 'Male')
    TYPE2 = ('FEM', 'Female')
    TYPE3 = ('OTHER', 'Other')

    @classmethod
    def choices(cls):
        return [(choice.value[0], choice.value[1]) for choice in cls]

class ContributionCode(Enum):
        STANDARD = ('S', 'Standard')
        SELF_EMPLOYED = ('D', 'Self Employed/Non Employed/Prescribed')
        GOVERNMENT_SHARE = ('G', 'Government Share')
        ONLY_NSF = ('N', 'Only NSF (Employer Share only)')
        NO_CONTRIBUTIONS = ('V', 'No Contributions')
        EXEMPTED = ('X', 'Exempted')

        def __init__(self, code, description):
            self.code = code
            self.description = description

        @classmethod
        def choices(cls):
            return [(choice.value[0], choice.value[1]) for choice in cls]


##Full-Time: Standard full-time work.
#Part-Time: Less than full-time hours, usually offering flexibility.
#Contract: Employment based on a contractual agreement for a specified period or project.
#Temporary: Often similar to contract but typically for short-term assignments.
#Internship: Training-oriented positions, usually temporary and sometimes unpaid.
#Freelance: Work on a per-job or gig basis, not necessarily tied to any single employer.
class EmploymentType(Enum):
    FULL_TIME = ('FULL', 'Full-Time')
    PART_TIME = ('PART', 'Part-Time')
    CONTRACT = ('CONT', 'Contract')
    TEMPORARY = ('TEMP', 'Temporary')
    INTERNSHIP = ('INTERN', 'Internship')
    FREELANCE = ('FREE', 'Freelance')

    def __init__(self, code, description):
        self.code = code
        self.description = description

    @classmethod
    def choices(cls):
        return [(choice.value[0], choice.value[1]) for choice in cls]



class AmountSplitType(Enum):
    TYPE1 = ('PERCENT', 'Percentage')
    TYPE2 = ('FIXED_AMOUNT', 'Fixed Amount')

    @classmethod
    def choices(cls):
        return [(choice.value[0], choice.value[1]) for choice in cls]


class LeaveType(Enum):
    TYPE1 = ('SICK', 'Sick')
    TYPE2 = ('LOCAL', 'Local')
    TYPE3 = ('MAT', 'Maternity')

    @classmethod
    def choices(cls):
        return [(choice.value[0], choice.value[1]) for choice in cls]
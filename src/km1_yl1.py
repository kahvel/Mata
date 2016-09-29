# 'encoding=UTF-8'

import operator

# Defineerime Pythonis maatriksi.
# Palju näitekoodi on ette antud. Ise peate defineerima 4 funktsiooni, mille ette on märgitud TODO:

# Siis saame luua maatrikseid nii:
# minu_maatriks = Matrix([[1,2],[3,4]])
# st defineerin maatriksi kujul
# [[1, 2],
#  [3, 4]]

# Ja kui oleme defineerinud ka vastavad meetodid (= funktsioonid), saame teha maatriksitega tehteid,
# arvutada pöördmaatriksit, lahendada võrrandeid jms.


class Matrix(object):

    # Seda meetodit (= funktsiooni) kasutatakse uue maatriksi loomisel. Ehk kui ma kirjutan
    # minu_maatriks = Matrix([[1,2],[3,4]])
    # siis minnakse __init__ meetodi sisse ja väärtustatakse vajalikud muutujad.
    # Meetodi esimene argument on alati self. Self on see maatriks ise, mille muutujaid me defineerime.
    # Selfi kasutatakse selleks, et teiste meetodite sees siin defineeritud muutujaid kätte saada.
    def __init__(self, elements):
        self.row_count = len(elements)
        self.col_count = len(elements[0])
        self.elements = []
        for row in elements:
            self.elements.append(row[:])  # [:] tähendab, et kopeerime row elemendid.

    # See funktsioon kutsutakse välja, kui maatriksile midagi liidetakse (maatriks1 + maatriks2).
    # Sel juhul self on maatriks1 ja other on maatriks2. Other maatriksi elemendid saame kätte samamoodi, nagu self puhul (ehk other.elements).
    # Funktsiooni tagastus on tehte tulemus.
    def __add__(self, other):
        result_matrix_elements = []
        for self_row, other_row in zip(self.elements, other.elements):
            result_row = []
            for self_elem, other_elem in zip(self_row, other_row):
                result_row.append(self_elem + other_elem)
            result_matrix_elements.append(result_row)
        return Matrix(result_matrix_elements)

    # See funktsioon kutsutakse välja, kui maatriks sõneks teisendatakse (näiteks kui teeme print maatriks).
    def __repr__(self):
        return "\n".join(map(str, self.elements))

    # See funktsioon kutsutakse välja, kui maatriksid millegiga võrreldakse (näiteks maatriks1 == maatriks2).
    def __eq__(self, other):
        return self.elements == other.elements

    # Annab koopia maatriksi i-ndast reast.
    def get_row(self, i):
        return self.elements[i][:]

    # Annab koopia maatriksi j-ndast veerust.
    def get_col(self, j):
        return list(map(operator.itemgetter(j), self.elements))

    # TODO: Defineeri ise lahutamine (analoogiliselt liitmisega)
    def __sub__(self, other):
        return

    # TODO: Defineeri maatriksi (self) skalaariga korrutamine. Tagasta skalaariga korrutatud maatriks. Self maatriksi elemente ära muuda.
    def scalar_muliplication(self, scalar):
        return

    # TODO: Defineeri ise maatriksi (self) transponeerimine. Tagasta transponeeritud maatriks. Self maatriksi elemente ära muuda.
    def transposed(self):
        return

    # TODO: Defineeri ise maatriksite self ja other korrutamine (kutsutakse välja näiteks kui teeme maatriks1 * maatriks2). Tagasta korrutamise tulemus.
    def __mul__(self, other):
        return


# Kui oled funktsioonid defineerinud, saame testida

maatriks1 = Matrix([[1,2],[3,4]])
maatriks2 = Matrix([[4,3],[2,1]])
print "maatriks1:"
print maatriks1
print "\nmaatriks2:"
print maatriks2
print "\nSumma:"
print maatriks1 + maatriks2
print "\nVahe:"
print maatriks1 - maatriks2
print "\nSkalaariga korrutamine:"
print maatriks1.scalar_muliplication(3)
print "\nTransponeerimine:"
print maatriks1.transposed()
print "\nKorrutamine:"
print maatriks1 * maatriks2


import csv
import os
from PyQt6.QtWidgets import *
from gui import *

class Logic(QMainWindow, Ui_mainWindow):
    id_list = []
    votes = {}

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.submit_button.clicked.connect(lambda : self.submit())

    def get_voter_id(self) -> int | None:
        """
        method to validate and return the voter ID
        :return: id_num
        """
        id_num = self.voter_ID.text().strip()

        try:
            id_num = int(id_num)
        except ValueError:
            self.exception_label.setStyleSheet('color: red;')
            self.exception_label.setText('ID must be a number')
            return None
        return id_num

    def get_candidate(self) -> str | None:
        """
        method that checks radio buttons for input
        will also capitalize and validate the name if a third party was selected
        :return: candidate
        """
        if self.jane_radioButton.isChecked():
            candidate = "Jane"
        elif self.john_radioButton.isChecked():
            candidate = "John"
        elif self.third_party_radioButton.isChecked():
            candidate = self.third_party_entry.text().strip().capitalize()
        else:
            self.exception_label.setStyleSheet('color: red;')
            self.exception_label.setText("Please select a candidate")
            return None

        if candidate and candidate.isalpha():#validates the string is not empty and is a regular name
            return candidate
        else:
            self.exception_label.setStyleSheet('color: red;')
            self.exception_label.setText('Invalid 3rd party name')
            return None


    def submit(self) -> None:
        """
        method that calls the voter_id and candidate functions to access their values and adds to voters dictionary
        Voter ID is validated so the same ID can't vote more than once
        A CSV file is then generated and appends any additional names and increments votes for each candidate
        :return: None
        """
        id_num = self.get_voter_id()
        candidate = self.get_candidate()

        if id_num is None:#allows program to keep running until a valid voter ID is given
            return

        if candidate is None:
            return

        if id_num in self.id_list:#validates if the ID has been used. If not, then the ID is logged and can't be used again
            self.exception_label.setStyleSheet('color: red;')
            self.exception_label.setText('ID number has already voted')
            return
        else:
            self.id_list.append(id_num)


        self.exception_label.setStyleSheet('color: green;')
        self.exception_label.setText('Your vote has been cast')

        file_name = 'total_votes.csv'

        if os.path.exists(file_name):#checks if file already exists
            with open(file_name, 'r', newline='') as file:
                reader = csv.DictReader(file)#built-in method to read row as dictionary key:value (found on https://docs.python.org/3/library/csv.html)
                for row in reader:#Takes data from existing csv and reads it into the 'votes' dictionary
                    name = row['Candidate']
                    votes = int(row['Votes'])
                    self.votes[name] = votes#loads all previous values from last instance to the dictionary

        if candidate in self.votes:
            self.votes[candidate] += 1
        else:
            self.votes[candidate] = 1

        with open(file_name, 'w', newline='')as file:#updates dictionary data to the CSV file
            content = csv.writer(file)
            content.writerow(['Candidate', 'Votes'])
            for candidate, votes in self.votes.items():
                content.writerow([candidate, votes])

        self.voter_ID.clear()#block clears all inputs and radio buttons and puts cursor back in ID input
        self.third_party_entry.clear()

        if self.buttonGroup1.checkedButton() is not None:
            self.buttonGroup1.setExclusive(False)
            self.buttonGroup1.checkedButton().setChecked(False)
            self.buttonGroup1.setExclusive(True)

        self.voter_ID.setFocus()

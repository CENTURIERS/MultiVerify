class BiometricModality:
    """
    Klasa bazowa (interfejs) dla wszystkich modalności.
    Każda nowa modalność (twarz, głos itp.) musi po niej dziedziczyć
    i napisać te metody po swojemu.
    """
    
    def extract_features(self, file_path):
        """
        Wczytuje plik i wyciąga z niego cechy charakterystyczne (np. wektor liczb).
        """
        raise NotImplementedError("Musisz zaimplementować metodę extract_features!")

    def verify(self, features_a, features_b):
        """
        Porównuje dwa wektory cech i zwraca wynik podobieństwa (liczbę od 0 do 1).
        """
        raise NotImplementedError("Musisz zaimplementować metodę verify!")

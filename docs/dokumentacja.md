# DrobnaPomoc.pl – dokumentacja projektowa PZSP2

**Wersja V2** · 26.10.2026 · semestr 26Z  
**Zespół nr 18:** Jakub Adamczyk, Magdalena Sałuda, Bartosz Paszkiewicz, Patryk Nisgorski  
**Mentor zespołu:** Krystian Radlak · **Właściciel tematu:** Izabela Żółtkowska

## Spis treści

- 1 Wprowadzenie
  - 1.1 Cel projektu
  - 1.2 Wymagane pojęcia
  - 1.3 Wstępna wizja projektu
    - 1.3.1 Model finansowy
    - 1.3.2 Wycena zlecenia (propozycja zespołu – do weryfikacji z właścicielem tematu)
- 2 Metodyka wytwarzania
- 3 Analiza wymagań
  - 3.1 Wymagania użytkownika i biznesowe
    - 3.1.1 Wymagania biznesowe
    - 3.1.2 Wymagania użytkowe
    - 3.1.3 Wymagania systemowe
  - 3.2 Wymagania funkcjonalne i niefunkcjonalne
    - 3.2.1 Wymagania funkcjonalne
    - 3.2.2 Wymagania niefunkcjonalne
  - 3.3 Przypadki użycia
    - 3.3.1 Poziom ogólny (Aktorzy i wykaz przypadków użycia)
    - 3.3.2 Scenariusze na poziomie rozszerzonym
    - 3.3.3 Scenariusze wyjątkowe
  - 3.4 Potwierdzenie zgodności wymagań
- 4 Definicja architektury
- 5 Dane trwałe
  - 5.1 Model logiczny danych
  - 5.2 Przetwarzanie i przechowywanie danych
- 6 Specyfikacja analityczna i projektowa
- 7 Projekt standardu interfejsu użytkownika
- 8 Specyfikacja testów
- 9 Wirtualizacja/konteneryzacja
- 10 Bezpieczeństwo
- 11 Podręcznik użytkownika
- 12 Podręcznik administratora
- 13 Podsumowanie
- 14 Bibliografia

## 1 Wprowadzenie

### 1.1 Cel projektu

Celem projektu jest zaprojektowanie i wykonanie aplikacji webowej DrobnaPomoc.pl - platformy umożliwiającej szybkie i bezpieczne zamawianie drobnych usług lokalnych (zakupy, drobne naprawy, odśnieżanie, wyprowadzanie psa, montaż mebli, pomoc z komputerem itp.). Główną grupą odbiorców są seniorzy i osoby mniej sprawne cyfrowo oraz osoby zlecające usługę dla kogoś bliskiego, kto mieszka w innym miejscu.

System ma obsłużyć pełen proces realizacji usługi:

**potrzeba → zlecenie → weryfikacja → znalezienie wykonawcy → wykonanie → potwierdzenie → ewentualna poprawka → ocena.**

### 1.2 Wymagane pojęcia

| **Pojęcie** | **Znaczenie** |
|---|---|
| Zlecenie | Prośba o wykonanie usługi: kategoria, opis, termin realizacji i adres. Składa je zleceniodawca lub konsultant na jego rzecz. |
| Zakres usług | To, co wykonawca robi i gdzie, np. naprawy hydrauliczne i montaż mebli. Część profilu wykonawcy. |
| Oferta | Odpowiedź wykonawcy na konkretne zlecenie z ceną. Zleceniodawca wybiera jedną z ofert. |
| Zleceniodawca | Użytkownik składający zlecenie dla siebie. |
| Zleceniodawca zdalny | Użytkownik składający zlecenie dla innej osoby, podając jej dane w formularzu. |
| Profil wykonawcy | Kategorie usług, w których działa wykonawca, oraz jego oceny. |
| Weryfikacja wykonawcy | Konsultant przeprowadza rozmowę telefoniczną lub wideo z wykonawcą, podczas której potwierdza jego tożsamość i doświadczenie. Po pozytywnej weryfikacji konsultant zatwierdza konto. Do tego czasu wykonawca nie może przeglądać zleceń ani składać ofert. |
| Kod wizyty | Jednorazowy 4-cyfrowy kod, którym zleceniodawca potwierdza tożsamość wykonawcy przy drzwiach. |
| Potwierdzenia: P1 / P2 | Dwa potwierdzenia zleceniodawcy: czy praca została wykonana (P1) i czy wykonano ją prawidłowo (P2). |

### 1.3 Wstępna wizja projektu

| **Rola** | **Kto to jest** | **Co robi w systemie** |
|---|---|---|
| Klient (senior lub członek rodziny) | Senior lub inna osoba potrzebująca pomocy; docelowo każdy, kto potrzebuje usługi. | Zamawia usługę dla siebie lub kogoś, śledzi jej status, potwierdza wizytę i wykonanie, płaci, ocenia. |
| Wykonawca | Osoba świadcząca usługi. | Uzupełnia profil wykonawcy (kategorie usług i lokalizacje, w których działa), przechodzi weryfikację, przegląda aktualne zlecenia i składa do nich oferty z ceną, a po wybraniu jego oferty realizuje wizytę potwierdzoną kodem i zgłasza wykonanie pracy. |
| Konsultant | Pracownik DrobnaPomoc odpowiedzialny za bieżącą obsługę zleceń i kontakt z użytkownikami. | Przeprowadza rozmowy weryfikacyjne z nowymi wykonawcami i zatwierdza ich konta, przyjmuje zlecenia telefoniczne, dobiera wykonawców do zleceń, rozpatruje reklamacje oraz kontaktuje się ze zleceniodawcami, którzy nie potwierdzili wykonania usługi. |
| Administrator | Pracownik DrobnaPomoc odpowiedzialny za zarządzanie kontami i konfigurację platformy. | Blokuje i odblokowuje użytkowników naruszających regulamin, nadaje i zabiera uprawnienia pracownikom (np. rolę konsultanta), zarządza kategoriami usług oraz ustawia parametry systemu, takie jak stawka prowizji i wagi rankingu wykonawców. |

DrobnaPomoc.pl jest responsywną aplikacją webową, dostępną z poziomu przeglądarki na komputerach i smartfonach. Backend systemu udostępnia interfejs API REST, który umożliwia późniejsze podłączenie natywnych aplikacji mobilnych bez konieczności przebudowy systemu.

System składa się z części przeznaczonej dla użytkowników (zleceniodawca, zleceniodawca zdalny, wykonawca), dostępnej z jednego konta z możliwością przełączania ról, oraz z paneli dla pracowników platformy: konsultanta i administratora.

Składanie zleceń na rzecz seniorów może odbywać się na trzy sposoby: samodzielnie przez samego seniora za pośrednictwem platformy, za pośrednictwem zleceniodawcy zdalnego, który zamawia usługę na jego rzecz oraz poprzez kontakt telefoniczny z konsultantem.

Integracja panelu konsultanta z systemem telefonii SuperVoIP nie jest realizowana w ramach obecnego zakresu projektu ze względu na ograniczenia czasowe zespołu.

Główny proces biznesowy obejmuje następujące etapy: złożenie zlecenia → złożenie ofert przez zweryfikowanych wykonawców → wybór oferty przez zleceniodawcę lub przypisanie wykonawcy przez konsultanta → potwierdzenie tożsamości wykonawcy kodem wizyty → potwierdzenie wykonania (P1) i jakości usługi (P2) → ocena wykonawcy.

Kluczowe założenia logiki biznesowej systemu obejmują:

- **Jeden profil, wiele ról:** Użytkownik korzysta z jednego głównego konta, w ramach którego może płynnie przełączać się pomiędzy modułami (m.in. zleceniodawcy i wykonawcy).
- **Zamówienia zdalne:** Zleceniodawca zdalny może zamówić usługę na rzecz innej osoby (odbiorcy), wpisując jej dane w formularzu zlecenia. Odbiorca nie musi posiadać konta w systemie. Zakładamy, że zleceniodawca zdalny będzie zamawiał usługi przede wszystkim dla osób najmniej sprawnych cyfrowo, które zazwyczaj nie korzystają z aplikacji. Dlatego zlecenie nie jest powiązane z kontem odbiorcy, nawet jeśli odbiorca takie konto posiada - nie jest ono dla niego widoczne w systemie. Zlecenie w całości obsługuje zleceniodawca zdalny: śledzi jego status, przekazuje odbiorcy kod wizyty i potwierdza wykonanie usługi.
- **Prywatność i weryfikacja:** Do realizacji zleceń dopuszczani są wyłącznie zatwierdzeni przez konsultanta wykonawcy. Pełny adres realizacji jest domyślnie ukryty i ujawniany wykonawcy dopiero po formalnym zaakceptowaniu jego oferty przez zleceniodawcę.
- **Bezpieczeństwo wizyty:** Proces rozpoczęcia pracy w miejscu realizacji wymaga autoryzacji przy użyciu wygenerowanego przez system, jednorazowego 4-cyfrowego kodu, który wykonawca przekazuje zleceniodawcy.
- **Dwuetapowy odbiór usług (P1/P2):** Zakończenie zlecenia wymaga dwukrokowego potwierdzenia przez klienta - samego faktu wykonania pracy (P1) oraz jej należytej jakości i braku konieczności poprawek (P2). Brak odpowiedzi klienta nie oznacza automatycznej akceptacji i wymaga interwencji konsultanta.
- **Asysta operacyjna:** Konsultanci posiadają uprawnienia do ręcznej interwencji w cykl życia zlecenia (m.in. ręczne przydzielanie wykonawców w przypadku braku ofert, wprowadzanie zgłoszeń telefonicznych oraz rozstrzyganie sporów reklamacyjnych).

#### 1.3.1 Model finansowy

Przychód platformy pochodzi z prowizji pobieranej od wykonawców. Szczegółowe zasady rozliczeń opisano poniżej.

Platforma utrzymuje się z prowizji pobieranej od wykonawców; wykonawcy nie płacą abonamentu. Prowizja jest procentem ceny usługi, a jej stawkę ustala administrator w ustawieniach systemu.

Cena podana w ofercie jest kwotą końcową, którą płaci zleceniodawca - prowizja jest w niej zawarta i potrącana wykonawcy.

Zleceniodawca wybiera jedną z dwóch form płatności:

- Płatność online: zleceniodawca płaci przy wyborze oferty, a środki są blokowane do zakończenia usługi. Po potwierdzeniu wykonania (P1) naliczana jest prowizja platformy, a po potwierdzeniu jakości (P2) pozostała kwota jest wypłacana wykonawcy. W przypadku reklamacji wypłata zostaje wstrzymana do jej rozpatrzenia.

- Płatność gotówką: po wyborze jego oferty wykonawca wpłaca prowizję z góry, ponieważ przy tej formie płatności pieniądze nie przechodzą przez platformę. Dopiero wtedy otrzymuje pełny adres realizacji. Po wykonaniu usługi zleceniodawca płaci mu na miejscu całą kwotę ustaloną w ofercie. Jeśli zlecenie nie dojdzie do skutku, wpłacona prowizja jest wykonawcy zwracana.

Każda zmiana ceny po wyborze oferty wymaga ponownej akceptacji zleceniodawcy i przeliczenia prowizji. W pierwszym etapie projektu wszystkie operacje finansowe są realizowane w formie symulacji, bez rzeczywistych przepływów pieniędzy.

#### 1.3.2 Wycena zlecenia (propozycja zespołu – do weryfikacji z właścicielem tematu)

Sposób ustalania ceny zależy od kanału, którym złożono zlecenie:

- Zlecenie telefoniczne: konsultant w trakcie rozmowy wycenia zlecenie i potwierdza termin realizacji, dzięki czemu osoba dzwoniąca od razu otrzymuje informację o koszcie i terminie usługi. Następnie konsultant przypisuje wykonawcę, który realizuje zlecenie w ustalonej cenie.

- Zlecenie złożone w aplikacji: zleceniodawca od razu po wybraniu kategorii widzi szacunkowy koszt usługi w postaci widełek cenowych. Dokładną cenę i termin podają wykonawcy w ofertach, spośród których zleceniodawca wybiera jedną.

Widełki cenowe dla każdej kategorii usług są początkowo ustalane przez administratora, a w miarę gromadzenia danych mogą być wyznaczane na podstawie cen zrealizowanych zleceń.

Takie rozwiązanie pozwala osobom korzystającym z telefonu od razu poznać wiążącą cenę, a użytkownikom aplikacji porównać oferty kilku wykonawców. Ze względu na to, że odbiega ono od pierwotnego założenia o wycenie każdego zlecenia przez konsultanta, wymaga potwierdzenia przez właściciela tematu.

## 2 Metodyka wytwarzania

Do realizacji projektu wybrano model kaskadowy (Waterfall). Prace zespołu są realizowane w ściśle określonych, następujących po sobie fazach (analiza wymagań, projektowanie, implementacja, testowanie). Na początku projektu zespół zaplanował wszystkie zadania i stworzył specyfikację, opierając się na priorytetach MoSCoW (rozdz. 3.2). Realizacja planu jest koordynowana na wewnętrznych spotkaniach zespołu, a postępy śledzone są zgodnie z głównym harmonogramem ustalonym na początku procesu implementacji.

Spotkania z właścicielem tematu odbywały się na etapie zbierania i zatwierdzania wymagań. Obecnie zespół kontaktuje się z właścicielem tematu głównie w przypadku pojawienia się problemów lub wątpliwości dotyczących specyfikacji, a także w celu formalnego odbioru gotowych etapów projektu (kamieni milowych). Dodatkowo, po zakończeniu każdej z głównych faz projektu, właściciel tematu otrzymuje wiadomość e-mail z oficjalnym podsumowaniem zrealizowanych prac.

Kod źródłowy jest tworzony w fazie implementacji i przechowywany w repozytorium Git na platformie GitHub. Każdy moduł systemu jest rozwijany na osobnej gałęzi i trafia do gałęzi głównej po rygorystycznym przeglądzie kodu przez innego członka zespołu.

## 3 Analiza wymagań

### 3.1 Wymagania użytkownika i biznesowe

#### 3.1.1 Wymagania biznesowe

Głównym problemem biznesowym jest potrzeba pomocy w drobnych pracach domowych wśród osób starszych i wykluczonych cyfrowo, połączona z obawą przed wpuszczaniem do domu nieznajomych. Dodatkową potrzebą jest wsparcie bliskich w organizowaniu pomocy udzielanej przez osoby trzecie, w tym bieżący nadzór nad jej realizacją. Wymagania biznesowe (WB) obejmują:

| **ID** | **Nazwa** | **Opis** |
|---|---|---|
| WB-01 | Dostępność usług | Udostępnienie platformy internetowej, dostępnej przez przeglądarkę na komputerze i smartfonie, ułatwiającej zamawianie drobnych usług. Osoby niekorzystające z internetu mogą składać zlecenia telefonicznie za pośrednictwem konsultanta. |
| WB-02 | Bezpieczeństwo użytkowników | Zapewnienie bezpieczeństwa zleceniodawców na każdym etapie realizacji usługi poprzez weryfikację wykonawców, potwierdzanie ich tożsamości przy wizycie, ochronę danych osobowych oraz rozliczenie usługi dopiero po potwierdzeniu jej wykonania. |
| WB-03 | Obsługa pełnego procesu zlecenia | Umożliwienie obsługi całego procesu realizacji usługi: złożenie zlecenia, wybór wykonawcy, wykonanie usługi przez wykonawcę, potwierdzenie realizacji, ewentualna reklamacja i ocena wykonawcy. |
| WB-04 | Organizowanie pomocy przez bliskich | Umożliwienie bliskim organizowania pomocy dla osoby starszej, w tym zamawiania usług na jej rzecz oraz bieżącego nadzoru nad ich realizacją, również na odległość. |
| WB-05 | Wsparcie użytkowników przez konsultanta | Zapewnienie użytkownikom, zwłaszcza osobom mniej sprawnym cyfrowo, pomocy pracownika platformy na każdym etapie realizacji usługi – w szczególności, gdy samodzielne skorzystanie z platformy jest utrudnione lub pojawi się problem z wykonaną usługą. |

#### 3.1.2 Wymagania użytkowe

System obsługuje różne grupy interesariuszy: klientów docelowych, ich rodziny/opiekunów, wykonawców usług, konsultantów i administratorów. Wymagania użytkowe (WU) to:

| **ID** | **Aktor** | **Opis wymagania** | **Powiązanie** |
|---|---|---|---|
| **Wszyscy użytkownicy** | | | |
| WU-01 | Gość | Może założyć konto, podając imię, nazwisko, adres e-mail, numer telefonu i hasło. Rejestracja wymaga akceptacji regulaminu i zgody na przetwarzanie danych osobowych zgodnie z RODO; konto jest aktywne po potwierdzeniu adresu e-mail. | WB-01, WB-02 |
| WU-02 | Użytkownik | Może zalogować się adresem e-mail i hasłem oraz zresetować zapomniane hasło. | WB-01 |
| WU-03 | Użytkownik | Może przeglądać i edytować swoje dane, wycofać zgodę na przetwarzanie danych oraz zażądać usunięcia konta. | WB-02 |
| WU-04 | Użytkownik | Może przełączać się w ramach jednego konta między rolami zleceniodawcy, zleceniodawcy zdalnego i wykonawcy. | WB-01 |
| WU-05 | Użytkownik | Na każdym ekranie widzi numer telefonu do konsultanta. | WB-01, WB-05 |
| WU-06 | Użytkownik | Korzysta z interfejsu dostosowanego do osób starszych: duże czcionki i przyciski. | WB-01, WB-05 |
| **Zleceniodawca** | | | |
| WU-07 | Zleceniodawca | Może złożyć zlecenie, podając kategorię, opis, termin realizacji i adres oraz opcjonalnie zdjęcie. Po wybraniu kategorii widzi szacunkowy koszt usługi w postaci widełek cenowych. | WB-01, WB-03 |
| WU-08 | Zleceniodawca | Może przeglądać oferty złożone do swojego zlecenia i wybrać jedną z nich wraz z formą płatności (online lub gotówka). | WB-03 |
| WU-09 | Zleceniodawca | Może śledzić status zlecenia, a po przypisaniu wykonawcy widzi jego imię, zdjęcie i termin wizyty. Kod wizyty jest udostępniany po zaakceptowaniu oferty wybranego wykonawcy. | WB-02, WB-03 |
| WU-10 | Zleceniodawca | Może anulować zlecenie przed zaakceptowaniem oferty wykonawcy. | WB-03 |
| WU-11 | Zleceniodawca | Może potwierdzić wykonanie (P1) i jakość pracy (P2) albo zgłosić reklamację. | WB-02, WB-03 |
| WU-12 | Zleceniodawca | Może ocenić wykonawcę w skali 1–5 i dodać komentarz. | WB-03 |
| **Zleceniodawca zdalny** | | | |
| WU-13 | Zleceniodawca zdalny | Może złożyć zlecenie dla odbiorcy, podając jego imię, nazwisko, numer telefonu i adres oraz potwierdzając, że odbiorca zgodził się na przekazanie swoich danych i wizytę wykonawcy. | WB-02, WB-04 |
| WU-14 | Zleceniodawca zdalny | Może złożyć zlecenie także dla odbiorcy posiadającego konto w systemie - dane odbiorcy są wtedy wprowadzane tak samo jak w WU-13.<br>Zleceniem zarządza zleceniodawca zdalny. | WB-04 |
| WU-15 | Zleceniodawca zdalny | W odniesieniu do złożonego przez siebie zlecenia ma te same możliwości co zleceniodawca (od WU-08 do WU-12). | WB-04 |
| WU-16 | Zleceniodawca zdalny | Może zapisać dane odbiorcy i wybierać go z listy przy kolejnych zleceniach. | WB-04 |
| WU-17 | Zleceniodawca zdalny | Otrzymuje powiadomienia o zmianach statusu zlecenia, w tym o przypisaniu wykonawcy, rozpoczęciu i zakończeniu wizyty. | WB-04 |
| WU-18 | Zleceniodawca zdalny | Przekazuje odbiorcy kod wizyty otrzymany w systemie w dogodny dla nich sposób (np. telefonicznie lub SMS-em); system nie wysyła kodu bezpośrednio do odbiorcy. | WB-02, WB-04 |
| **Wykonawca** | | | |
| WU-19 | Wykonawca | Może uzupełnić profil wykonawcy: zakres usług (kategorie usług oraz obszar działania - miasto i dzielnice wybrane z listy) oraz zdjęcie. | WB-03 |
| WU-20 | Wykonawca | Po weryfikacji może przeglądać zlecenia zgodne ze swoim zakresem usług (bez pełnego adresu) i składać do nich oferty z ceną i proponowanym terminem wizyty oraz wycofywać oferty, dopóki nie zostaną wybrane. | WB-02, WB-03 |
| WU-21 | Wykonawca | Przy płatności gotówkowej, po zaakceptowaniu oferty przez zleceniodawcę, wpłaca (w formie symulacji) prowizję, po której otrzymuje pełny adres realizacji. | WB-02, WB-03 |
| WU-22 | Wykonawca | Może przyjąć lub odrzucić przypisanie do zlecenia zaproponowane przez konsultanta. | WB-03 |
| WU-23 | Wykonawca | Może rozpocząć wizytę po potwierdzeniu kodu wizyty przez odbiorcę i zgłosić zakończenie pracy. | WB-02 |
| WU-24 | Wykonawca | Może przeglądać historię swoich zleceń, ocen i rozliczeń. | WB-03 |
| **Konsultant** | | | |
| WU-25 | Konsultant | Może przeprowadzić z wykonawcą rozmowę weryfikacyjną (telefoniczną lub wideo), podczas której potwierdza jego tożsamość i doświadczenie, a następnie zatwierdzić jego konto albo je odrzucić. | WB-02 |
| WU-26 | Konsultant | Może złożyć zlecenie na rzecz osoby dzwoniącej, wpisując jej dane (imię, nazwisko, telefon, adres) w formularzu zlecenia po uzyskaniu ustnej zgody na przetwarzanie danych, a następnie w trakcie rozmowy wycenić zlecenie i potwierdzić termin realizacji. Dane nie są zapisywane jako osobny profil. | WB-01, WB-05 |
| WU-27 | Konsultant | Przekazuje kod wizyty telefonicznie osobie, dla której przyjął zlecenie. | WB-02, WB-05 |
| WU-28 | Konsultant | Może przypisać wykonawcę do zlecenia, korzystając z listy kandydatów uszeregowanej według rankingu. | WB-03, WB-05 |
| WU-29 | Konsultant | Może rozpatrywać reklamacje: zlecić poprawkę albo zamknąć zlecenie. | WB-02, WB-05 |
| WU-30 | Konsultant | Obsługuje kolejkę zleceń bez potwierdzenia P1 lub P2 i rejestruje w systemie próby kontaktu. | WB-02, WB-05 |
| **Administrator** | | | |
| WU-31 | Administrator | Może blokować i odblokowywać konta użytkowników, podając powód blokady. | WB-02 |
| WU-32 | Administrator | Może nadawać i odbierać pracownikom role konsultanta i administratora. | WB-02 |
| WU-33 | Administrator | Może dodawać, edytować i wyłączać kategorie usług. | WB-01 |
| WU-34 | Administrator | Może dodawać, edytować i wyłączać kategorie usług oraz ustalać dla nich początkowe widełki cenowe, obowiązujące do czasu zgromadzenia wystarczającej liczby zrealizowanych zleceń, na podstawie których system wyznacza widełki automatycznie. | WB-03 |

#### 3.1.3 Wymagania systemowe

Są to ramy techniczne i logiczne, w jakich platforma będzie funkcjonować jako produkt informatyczny. Wymagania systemowe (WS) obejmują:

| **ID** | **Opis** |
|---|---|
| WS-01 | Zbudowanie aplikacji w postaci responsywnego systemu webowego, działającego poprawnie w przeglądarkach na komputerach i smartfonach. |
| WS-02 | Zaprojektowanie backendu oraz interfejsów API w taki sposób, aby w przyszłości system obsługiwał natywne aplikacje mobilne. |
| WS-03 | Implementacja rozdzielonych, niezależnych słowników statusów dla kluczowych encji biznesowych: zlecenia, oferty, płatności oraz reklamacji. |
| WS-04 | Zastosowanie algorytmu rankingu wykonawców na liście ofert i przy przypisywaniu ręcznym, opartego na parametrach konfigurowalnych w systemie (średnia ocen, dopasowanie obszaru działania, historia współpracy). |
| WS-05 | Realizacja dwuetapowego modelu odbioru prac: P1 (potwierdzenie wykonania - podstawa naliczenia prowizji platformy) oraz P2 (potwierdzenie jakości - podstawa zwolnienia środków dla wykonawcy). |
| WS-06 | Symulacja przepływów rozliczeniowych: warunkowej płatności online z blokadą środków oraz płatności gotówkowej wymagającej wpłaty przez wykonawcę prowizji przed uzyskaniem pełnego adresu realizacji. |
| WS-07 | Wspólny backend z jedną bazą danych obsługujący część dla użytkowników oraz panele konsultanta i administratora. |
| WS-08 | Kontrola dostępu oparta na rolach, weryfikowana po stronie serwera przy każdej operacji, niezależnie od interfejsu użytkownika. |
| WS-09 | Mechanizm kodu wizyty: przed wizytą system udostępnia ten sam jednorazowy kod usługi zleceniodawcy i wykonawcy. Po przybyciu wykonawca podaje swój kod, a odbiorca porównuje go z kodem otrzymanym wcześniej w systemie. |
| WS-10 | Słowniki kategorii usług oraz obszarów działania (miasta i dzielnice) zarządzane przez administratora, wykorzystywane do dopasowania zleceń do wykonawców. |
| WS-11 | Rejestrowanie historii zmian zlecenia oraz decyzji administracyjnych (blokady, zmiany ról) z informacją o użytkowniku i jego roli. |
| WS-12 | Moduł wysyłki powiadomień e-mail o zmianach statusu zlecenia, nowych ofertach oraz przypomnień o wizycie. |

### 3.2 Wymagania funkcjonalne i niefunkcjonalne

Ze względu na budżet czasowy projektu (300 roboczogodzin) oraz zakres oczekiwań właściciela tematu, wyceniony przez zespół na ponad 600 roboczogodzin, wymagania zostały uszeregowane według priorytetów metodą MoSCoW. Tabele zawierają powiązania z wymaganiami zdefiniowanymi w rozdziale 3.1.

**Legenda priorytetów:**

**- M (Must have):** funkcjonalności niezbędne dla działania systemu w wersji MVP.

**- S (Should have):** funkcjonalności ważne, uwzględnione w planie zespołu, które mogą zostać uproszczone w przypadku opóźnień.

**- C (Could have):** usprawnienia realizowane w miarę dostępności czasu.

**- W (Won't have):** wymagania zgłoszone przez właściciela tematu, wykraczające poza budżet projektu, które mogą zostać zrealizowane w kolejnych etapach.

#### 3.2.1 Wymagania funkcjonalne

| **ID** | **Nazwa wymagania** | **Opis wymagania** | **Priorytet** | **Powiązanie** |
|---|---|---|---|---|
| WF-01 | Rejestracja i logowanie | System umożliwia rejestrację z akceptacją regulaminu i zgodą na przetwarzanie danych, potwierdzenie adresu e-mail, logowanie e-mailem i hasłem oraz reset hasła. | Must have | WU-01, WU-02 |
| WF-02 | Zarządzanie danymi konta | System umożliwia edycję danych użytkownika, wycofanie zgody na przetwarzanie danych i usunięcie konta. | Must have | WU-03 |
| WF-03 | Przełącznik ról | System umożliwia przełączanie kontekstu między rolami zleceniodawca, zleceniodawca zdalny i wykonawca w ramach jednego konta. | Must have | WU-04 |
| WF-04 | Kontakt z konsultantem | System wyświetla numer telefonu do konsultanta na każdym ekranie. | Must have | WU-05 |
| WF-05 | Składanie zlecenia | System umożliwia złożenie zlecenia (kategoria, opis, termin realizacji, adres z obszarem działania, opcjonalne zdjęcie) oraz jego anulowanie przed zaakceptowaniem przez wykonawcę. | Must have | WU-07, WU-10 |
| WF-06 | Zlecenie dla innej osoby | System umożliwia złożenie zlecenia z danymi odbiorcy wprowadzonymi w formularzu i potwierdzeniem jego zgody; zlecenie nie jest powiązane z kontem odbiorcy. | Must have | WU-13, WU-14, WU-15 |
| WF-07 | Zapisani odbiorcy | System umożliwia zapisanie danych odbiorców i wybór z listy przy kolejnych zleceniach. | Could have | WU-16 |
| WF-08 | Ofertowanie | System udostępnia zweryfikowanym wykonawcom zlecenia zgodne z ich zakresem usług (bez pełnego adresu) i umożliwia składanie oraz wycofywanie ofert z ceną i terminem wizyty. | Must have | WU-20 |
| WF-09 | Wybór oferty i przypisanie wykonawcy | System umożliwia wybór oferty i formy płatności przez zleceniodawcę albo przypisanie wykonawcy przez konsultanta, z akceptacją wykonawcy. | Must have | WU-08, WU-22, WU-28 |
| WF-10 | Kod wizyty | System generuje jednorazowy 4-cyfrowy kod wizyty i udostępnia go przed wizytą. | Must have | WU-09, WU-18, WU-23, WU-27 |
| WF-11 | Potwierdzenia P1 i P2 | System umożliwia zleceniodawcy dwuetapowe potwierdzenie wykonania i jakości pracy albo zgłoszenie reklamacji. | Must have | WU-11 |
| WF-12 | Kolejka braku odpowiedzi | Brak odpowiedzi na P1 lub P2 tworzy wpis w kolejce konsultanta, w którym rejestruje on próby kontaktu. | Should have | WU-30 |
| WF-13 | Symulacja płatności | System symuluje blokadę środków przy płatności online, naliczenie prowizji po P1, wypłatę po P2 oraz prowizję wykonawcy przy płatności gotówkowej. | Should have | WU-08, WU-21 |
| WF-14 | Osobne statusy | System prowadzi niezależne statusy zlecenia, oferty, płatności i reklamacji. | Must have | WU-09 |
| WF-15 | Ranking wykonawców | System szereguje oferty i kandydatów według konfigurowalnego wzoru (średnia ocen, obszar działania, historia współpracy). | Should have | WU-08, WU-28 |
| WF-16 | Zlecenie telefoniczne | System umożliwia konsultantowi tworzenia zlecenia na rzecz osoby dzwoniącej. | Must have | WU-26 |
| WF-17 | Weryfikacja wykonawców | System udostępnia konsultantowi listę kont oczekujących na weryfikację oraz umożliwia ich zatwierdzenie lub odrzucenie z podaniem powodu. | Must have | WU-25 |
| WF-18 | Reklamacje i oceny | System umożliwia zgłaszanie reklamacji i ich rozpatrywanie przez konsultanta oraz ocenę wykonawcy w skali 1-5 z komentarzem. | Should have | WU-11, WU-12, WU-29 |
| WF-19 | Status i historia zleceń | System prezentuje aktualny status zlecenia oraz historię zleceń, ocen i rozliczeń użytkownika. | Must have | WU-09, WU-24 |
| WF-20 | Panel administratora | System umożliwia blokowanie kont, nadawanie ról pracownikom oraz zarządzanie kategoriami usług, obszarami działania i parametrami systemu. | Must have | WU-31 – WU-34 |
| WF-21 | Powiadomienia e-mail | System wysyła powiadomienia e-mail o nowych ofertach, przypisaniu wykonawcy i zmianach statusu zlecenia oraz przypomnienia o wizycie. | Could have | WU-17 |
| WF-22 | Historia zmian | System rejestruje historię zmian zlecenia oraz decyzji administracyjnych z informacją o użytkowniku i jego roli. | Should have | WU-31, WU-32 |
| WF-23 | Integracja SuperVoIP | Automatyczne rozpoznawanie dzwoniącego, powiązanie rozmowy ze zleceniem i połączenia z panelu konsultanta. | Won't have | WB-05 |
| WF-24 | Rzeczywiste płatności | Produkcyjna integracja z operatorem płatności. | Won't have | WB-02 |
| WF-25 | Moduł AI | Automatyczna wycena zlecenia na podstawie zdjęcia. | Won't have | WB-03 |

#### 3.2.2 Wymagania niefunkcjonalne

| **ID** | **Nazwa wymagania** | **Opis wymagania** | **Priorytet** | **Powiązanie** |
|---|---|---|---|---|
| WNF-01 | Dostępność dla seniorów | Interfejs jest responsywny (komputery, smartfony) i dostosowany do osób starszych: duża czcionka i przyciski. | Must have | WU-06 |
| WNF-02 | Architektura pod aplikacje mobilne | Backend udostępnia udokumentowane API REST umożliwiające podłączenie natywnych aplikacji mobilnych bez przebudowy systemu. | Must have | WB-01 |
| WNF-03 | Poufność adresu | Pełny adres realizacji jest widoczny wyłącznie dla wykonawcy przypisanego do zlecenia po zabezpieczeniu płatności lub wpłacie prowizji. | Must have | WB-02, WU-20 |
| WNF-04 | Bezpieczeństwo | Hasła są przechowywane w postaci skrótu; uprawnienia są sprawdzane po stronie serwera przy każdej operacji. | Must have | WB-02 |
| WNF-05 | Ochrona danych osobowych (RODO) | Dane osobowe są przetwarzane zgodnie z RODO: system zbiera wyłącznie niezbędne dane, rejestruje udzielone zgody i umożliwia usunięcie konta wraz z danymi. | Must have | WB-02, WU-01, WU-03 |
| WNF-06 | Wydajność | Czas odpowiedzi systemu dla typowych operacji użytkownika nie przekracza 2 sekund. | Should have | WB-01 |
| WNF-07 | Natywne aplikacje mobilne | Aplikacje dla systemów Android i iOS. | Won't have | WB-01 |

### 3.3 Przypadki użycia

#### 3.3.1 Poziom ogólny (Aktorzy i wykaz przypadków użycia)

W systemie DrobnaPomoc zidentyfikowano pięciu głównych aktorów:

- **Zleceniodawca:** składa zlecenie dla siebie, wybiera ofertę, sprawdza tożsamość wykonawcy za pomocą kodu wizyty, odpowiada na pytania o wykonanie i jakość pracy (P1, P2) oraz opcjonalnie ocenia wykonawcę.
- **Zleceniodawca zdalny:** składa zlecenie dla odbiorcy, wprowadzając jego dane w formularzu, przekazuje mu kod wizyty, śledzi realizację zlecenia.
- **Wykonawca:** zweryfikowany usługodawca, który przegląda zlecenia zgodne ze swoim zakresem usług, składa oferty, realizuje wizytę i zgłasza wykonanie pracy.
- **Konsultant:** weryfikuje wykonawców, przyjmuje zlecenia telefoniczne, przypisuje wykonawców do zleceń, rozpatruje reklamacje i obsługuje zlecenia bez potwierdzenia.
- **Administrator:** blokuje i odblokowuje konta, nadaje role pracownikom oraz zarządza kategoriami usług, obszarami działania i parametrami systemu.

**Cykl życia zlecenia**

Zlecenie przechodzi przez dwa zasadniczo różne stany: zgłoszone (bez przypisanego wykonawcy) oraz przypisane (z wykonawcą). Pełny cykl statusów zlecenia przedstawia tabela.

| **Status** | **Opis** |
|---|---|
| Oczekuje na oferty | Zlecenie zgłoszone i przyjęte w systemie, bez przypisanego wykonawcy. Zawiera termin realizacji określony przez zleceniodawcę: konkretny dzień z porą dnia albo okres elastyczny („jak najszybciej”, „w ciągu 3 dni”, „w ciągu tygodnia”). Zlecenie jest widoczne dla zweryfikowanych wykonawców z pasującym zakresem usług. Wykonawcy widzą jedynie miasto i dzielnicę -pełny adres jest udostępniany wyłącznie wykonawcy przypisanemu do zlecenia. |
| Czeka na wykonawcę | Po 72 godzinach bez ofert albo na prośbę zleceniodawcy zlecenie trafia do konsultanta, który ręcznie szuka wykonawcy. |
| Wykonawca wybrany | Zlecenie przypisane do wykonawcy. Przypisania dokonuje zleceniodawca, wybierając ofertę (UC-03), albo konsultant (UC-04) - wtedy wymagana jest akceptacja wykonawcy i zatwierdzenie ceny przez zleceniodawcę. Warunkiem przypisania jest zabezpieczenie płatności (online) albo wpłata prowizji przez wykonawcę (gotówka). Po przypisaniu wykonawca otrzymuje pełny adres i termin wizyty, a zleceniodawca - dane wykonawcy i termin wizyty. Status pozostałych ofert złożonych do tego zlecenia zmienia się na „Odrzucona”. |
| W realizacji | Wykonawca rozpoczął wizytę po potwierdzeniu kodu wizyty. |
| Wykonane | Wykonawca zgłosił zakończenie pracy; system oczekuje na potwierdzenia P1 i P2. |
| Do poprawki | Zleceniodawca zgłosił reklamację; sprawę rozpatruje konsultant. |
| Zakończone | Zleceniodawca potwierdził P1 i P2 albo konsultant zamknął reklamację. |
| Anulowane | Zlecenie anulowane przez zleceniodawcę lub konsultanta przed przypisaniem wykonawcy. |

**Wykaz przypadków użycia (UC) z relacjami**

| **ID** | **Przypadek użycia** | **Aktorzy** |
|---|---|---|
| UC-01 | Składanie zlecenia | Zleceniodawca, Zleceniodawca zdalny |
| UC-02 | Wysyłanie oferty | Wykonawca |
| UC-03 | Wybór oferty | Zleceniodawca, Zleceniodawca zdalny |
| UC-04 | Ręczne przypisanie wykonawcy (UC-03) | Konsultant, Wykonawca |
| UC-05 | Przyjęcie zlecenia telefonicznego (UC-01, UC-04) | Konsultant |
| UC-06 | Bezpieczna wizyta | Wykonawca, Zleceniodawca, Zleceniodawca zdalny |
| UC-07 | Zakończenie, odbiór (P1/P2) i ocena | Zleceniodawca, Wykonawca, Konsultant |
| UC-08 | Rejestracja i weryfikacja wykonawcy | Wykonawca, Konsultant |
| UC-09 | Zablokowanie użytkownika | Administrator |

#### 3.3.2 Scenariusze na poziomie rozszerzonym

##### UC-01. Składanie zlecenia

| **Atrybut** | **Opis** |
|---|---|
| Aktor | Zleceniodawca, Zleceniodawca zdalny |
| Cel | Opisać potrzebę i wystawić zlecenie dla wykonawców. |
| Warunek początkowy | Użytkownik jest zalogowany w roli Zleceniodawcy lub Zleceniodawcy zdalnego. |
| Przebieg główny | 1. Użytkownik klika „Nowe zlecenie”.<br>2. Wybiera kategorię usługi (np. „Naprawy i montaż”), opisuje problem, opcjonalnie dodaje zdjęcie.<br>3. Zleceniodawca zdalny wybiera odbiorcę z listy zapisanych albo wpisuje jego dane (imię, nazwisko, telefon, adres) i potwierdza zgodę odbiorcy.<br>4. Określa termin realizacji: konkretny dzień z porą dnia albo okres elastyczny.<br>5. Podaje adres i wybiera z listy miasto i dzielnicę.<br>6. Sprawdza podsumowanie i wysyła zlecenie → status Oczekuje na oferty.<br>7. System udostępnia zlecenie wykonawcom z pasującym zakresem usług. |
| Sytuacje alternatywne | 2a. Użytkownik nie wie, jaką kategorię wybrać → wybiera „Inne” albo dzwoni do konsultanta.<br>Na każdym kroku użytkownik może zadzwonić do konsultanta. |
| Wynik | Zlecenie jest widoczne dla pasujących wykonawców, bez pełnego adresu. |

##### UC-02. Wysyłanie oferty

| **Atrybut** | **Opis** |
|---|---|
| Aktor | Wykonawca |
| Cel | Zgłosić gotowość wykonania zlecenia, podając cenę i termin wizyty. |
| Warunek początkowy | Wykonawca przeszedł weryfikację; zlecenie ma status „Oczekuje na oferty". |
| Przebieg główny | 1. Wykonawca widzi listę zleceń zgodnych ze swoim zakresem usług.<br>2. Otwiera zlecenie: opis, zdjęcie, termin realizacji, dzielnica (bez pełnego adresu).<br>3. Klika „Wyślij ofertę”, podaje cenę, proponowany termin wizyty i opcjonalny komentarz.<br>4. Zleceniodawca otrzymuje powiadomienie o nowej ofercie. |
| Sytuacje alternatywne | 3a. Wykonawca może wycofać ofertę, dopóki nie zostanie wybrana. |
| Wynik | Oferta trafia na listę ofert zlecenia. |

##### UC-03. Wybór oferty

| **Atrybut** | **Opis** |
|---|---|
| Aktor | Zleceniodawca, Zleceniodawca zdalny |
| Cel | Wybrać wykonawcę spośród złożonych ofert. |
| Warunek początkowy | Do zlecenia wpłynęła co najmniej jedna oferta. |
| Przebieg główny | 1. Zleceniodawca otwiera zlecenie i widzi listę ofert: imię i zdjęcie wykonawcy, cena, termin wizyty, średnia ocena, liczba wykonanych zleceń.<br>2. Lista jest uszeregowana według rankingu; zleceniodawca może ją posortować po cenie.<br>3. Zleceniodawca wybiera ofertę i formę płatności (online lub gotówka).<br>4. System symuluje zabezpieczenie środków (online) albo wykonawca wpłaca symulowaną prowizję (gotówka).<br>5. Status → Wykonawca wybrany. Wykonawca otrzymuje pełny adres i termin, a Status pozostałych ofert zmienia się na „Odrzucona”. |
| Sytuacje alternatywne | 1a. Brak ofert po 72 godzinach lub zleceniodawca prosi o pomoc → zlecenie trafia do konsultanta (UC-04).<br>3a. Żadna oferta nie odpowiada zleceniodawcy → może anulować zlecenie (status Anulowane). |
| Wynik | Zlecenie ma przypisanego wykonawcę, cenę, termin wizyty i formę płatności. |

##### UC-04. Ręczne przypisanie wykonawcy

| **Atrybut** | **Opis** |
|---|---|
| Aktor | Konsultant, Wykonawca |
| Cel | Przypisać wykonawcę, gdy zleceniodawca sam go nie wybrał. |
| Warunek początkowy | Zlecenie ma status Czeka na wykonawcę. |
| Przebieg główny | 1. Konsultant widzi zlecenie na liście „Czeka na wykonawcę”.<br>2. Klika „Dobierz wykonawcę”; system pokazuje kandydatów uszeregowanych według rankingu oraz dotychczasowe oferty.<br>3. Konsultant kontaktuje się z wybranym wykonawcą, ustala cenę i termin, a następnie przypisuje go do zlecenia.<br>4. Wykonawca akceptuje przypisanie, a zleceniodawca potwierdza cenę → dalej jak w UC-03, krok 4. |
| Sytuacje alternatywne | 2a. Brak kandydatów → konsultant poszerza obszar o sąsiednie dzielnice albo proponuje zleceniodawcy inny termin.<br>4a. Wykonawca odrzuca przypisanie → konsultant wybiera kolejnego kandydata. |
| Wynik | Zlecenie ma przypisanego wykonawcę. |

##### UC-05. Przyjęcie zlecenia telefonicznego

| **Atrybut** | **Opis** |
|---|---|
| Aktor | Konsultant |
| Cel | Przyjąć i obsłużyć zlecenie od osoby, która nie korzysta z aplikacji. |
| Warunek początkowy | Osoba dzwoni na infolinię DrobnaPomoc. |
| Przebieg główny | 1. Wypełnia formularz zlecenia na rzecz dzwoniącego (jak w UC-01).<br>2. Dobiera wykonawcę (jak w UC-04) i informuje dzwoniącego telefonicznie o terminie wizyty.<br>3. Przed wizytą przekazuje telefonicznie kod wizyty.<br>4. Po wizycie telefonicznie pyta o wykonanie i jakość pracy i wprowadza odpowiedzi P1 i P2 w systemie. |
| Sytuacje alternatywne |  |
| Wynik | Zlecenie jest obsługiwane w systemie tak samo jak złożone online. |

##### UC-06. Bezpieczna wizyta

| **Atrybut** | **Opis** |
|---|---|
| Aktor | Wykonawca, Zleceniodawca, Zleceniodawca zdalny |
| Cel | Odbiorca ma pewność, że przyszła właściwa osoba. |
| Warunek początkowy | Zlecenie ma status Wykonawca wybrany. |
| Przebieg główny | 1. Dzień przed wizytą zleceniodawca otrzymuje przypomnienie: termin oraz imię i zdjęcie wykonawcy.<br>2. Przed wizytą system udostępnia zleceniodawcy i wykonawcy kod wizyty. Zleceniodawca zdalny przekazuje kod odbiorcy w dogodny dla nich sposób.<br>3. Wykonawca przychodzi i podaje kod przy drzwiach lub przez domofon.<br>4. Odbiorca porównuje kod z otrzymanym i wpuszcza wykonawcę.<br>5. Wykonawca klika „Rozpocznij wizytę” → status W realizacji. |
| Sytuacje alternatywne | 4a. Kod się nie zgadza lub przyszła inna osoba → odbiorca nie otwiera i dzwoni do konsultanta. |
| Wynik | Rozpoczęcie wizyty jest zapisane w historii zlecenia, a kod wizyty wygasa. |

##### UC-07. Zakończenie, odbiór (P1/P2) i ocena

| **Atrybut** | **Opis** |
|---|---|
| Aktor | Wykonawca, Zleceniodawca, Konsultant |
| Cel | Potwierdzić wykonanie i jakość pracy oraz rozliczyć zlecenie. |
| Warunek początkowy | Zlecenie ma status "W realizacji". |
| Przebieg główny | 1. Wykonawca klika „Zakończ pracę”, opcjonalnie dodaje zdjęcie → status “Wykonane”.<br>2. Zleceniodawca odpowiada na pytanie P1 „Czy praca została wykonana?” → system symuluje naliczenie prowizji.<br>3. Zleceniodawca odpowiada na pytanie P2 „Czy praca została wykonana prawidłowo i nie wymaga poprawek?” → przy płatności online system symuluje wypłatę dla wykonawcy.<br>4. Zleceniodawca może ocenić wykonawcę w skali 1-5 i dodać komentarz → status “Zakończone”. |
| Sytuacje alternatywne | 2a/3a. Zleceniodawca odpowiada „Nie” → zgłasza reklamację, status “Do poprawki”, niewypłacone środki są wstrzymane. Konsultant rozpatruje reklamację: zleca poprawkę (powrót do kroku 1) albo zamyka zlecenie.<br>2b/3b. Brak odpowiedzi zleceniodawcy → zlecenie nie jest zamykane automatycznie; trafia do kolejki konsultanta, który rejestruje próby kontaktu. |
| Wynik | Zlecenie zakończone albo skierowane do poprawki. |

##### UC-08. Rejestracja i weryfikacja wykonawcy

| **Atrybut** | **Opis** |
|---|---|
| Aktor | Wykonawca, Konsultant |
| Cel | Dopuścić do zleceń wyłącznie sprawdzone osoby. |
| Warunek początkowy | Użytkownik ma konto i przełączył się na rolę Wykonawcy. |
| Przebieg główny | 1. Wykonawca uzupełnia profil: zakres usług (kategorie usług, miasto i dzielnice) oraz zdjęcie.<br>2. Konto wykonawcy otrzymuje status "Oczekuje na weryfikację" - wykonawca nie widzi zleceń i nie może składać ofert.<br>3. Konsultant przeprowadza z wykonawcą rozmowę telefoniczną lub wideo, podczas której potwierdza jego tożsamość i doświadczenie.<br>4. Konsultant klika „Zatwierdź”, wykonawca otrzymuje powiadomienie. |
| Sytuacje alternatywne | 4a. Konsultant odrzuca konto i podaje powód, wykonawca może uzupełnić profil i ponownie zgłosić go do weryfikacji. |
| Wynik | Wykonawca jest aktywny: widzi zlecenia zgodne ze swoim zakresem usług i może składać oferty. |

##### UC-09. Zablokowanie użytkownika

| **Atrybut** | **Opis** |
|---|---|
| Aktor | Administrator |
| Cel | Uniemożliwić korzystanie z systemu użytkownikowi naruszającemu regulamin. |
| Warunek początkowy | Administrator jest zalogowany. |
| Przebieg główny | 1. Administrator wyszukuje użytkownika na liście użytkowników.<br>2. Klika „Zablokuj” i podaje powód.<br>3. System oznacza konto jako zablokowane. W przypadku wykonawcy wycofuje jego otwarte oferty, a przypisane zlecenia przekazuje konsultantowi.<br>4. Przy próbie korzystania z systemu zablokowany użytkownik widzi komunikat o zablokowaniu konta wraz z powodem i numerem do konsultanta; nie może wykonać żadnej operacji. |
| Sytuacje alternatywne | 1a. Administrator może odblokować konto w tym samym panelu. |
| Wynik | Zablokowany użytkownik może się zalogować, ale nie ma dostępu do żadnych funkcji. |

#### 3.3.3 Scenariusze wyjątkowe

##### SC-01 Wykonawca nie stawia się na wizytę

Zgłoszenie nieobecności wykonawcy zmienia status wizyty na „Anulowana” wraz z podaniem powodu. Kod wizyty jest przypisany do konkretnej wizyty, dlatego wraz z jej anulowaniem przestaje być ważny. Zlecenie wraca do etapu wyboru wykonawcy, a nowa wizyta otrzymuje nowy kod. Rozliczenie nie jest uruchamiane.

##### SC-02 Pracy nie dało się wykonać

Wykonawca oznacza wizytę jako niemożliwą do wykonania i podaje powód, a status wizyty zmienia się na „Anulowana”. Zlecenie wraca do etapu wyboru wykonawcy, a nowa wizyta otrzymuje nowy kod. Pytanie P1 nie jest wysyłane, a prowizja nie jest naliczana.

##### SC-03 Praca wykonana częściowo

Konsultant zapisuje w sprawie wyjątkowej zakres wykonany, uzgodnioną kwotę i ewentualny termin poprawki. Korekta rozliczenia i prowizji jest zapisywana jako osobna operacja finansowa, bez nadpisywania historii.

##### SC-04 Odbiór P1/P2 i reklamacja

P1 i P2 są od siebie niezależne. Odpowiedź „Nie” na P1 przekazuje zlecenie konsultantowi do wyjaśnienia. Odpowiedź „Tak” na P1 i „Nie” na P2 otwiera reklamację, a wypłata dla wykonawcy zostaje wstrzymana. Gdy zleceniodawca nie odpowie, zlecenie trafia do kolejki konsultanta i nie jest automatycznie odebrane. Za jedno zlecenie prowizja może zostać naliczona tylko raz, także po poprawce.

### 3.4 Potwierdzenie zgodności wymagań

> Należy wkleić wycinek ekranu pokazujący korespondencję z Mentorem i Właścicielem tematu.

## 4 Definicja architektury

_Do uzupełnienia._

## 5 Dane trwałe

### 5.1 Model logiczny danych

_Do uzupełnienia._

### 5.2 Przetwarzanie i przechowywanie danych

_Do uzupełnienia._

## 6 Specyfikacja analityczna i projektowa

_Do uzupełnienia._

## 7 Projekt standardu interfejsu użytkownika

_Do uzupełnienia._

## 8 Specyfikacja testów

_Do uzupełnienia._

## 9 Wirtualizacja/konteneryzacja

_Do uzupełnienia._

## 10 Bezpieczeństwo

_Do uzupełnienia._

## 11 Podręcznik użytkownika

_Do uzupełnienia._

## 12 Podręcznik administratora

_Do uzupełnienia._

## 13 Podsumowanie

_Do uzupełnienia._

## 14 Bibliografia

_Do uzupełnienia._


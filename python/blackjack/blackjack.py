import random

card_flow = []                      #덱에서 꺼낸 카드를 잠시 보관
class Deck:
    def __init__(self):
        self.cards = []             #덱 생성시 카드 한벌을 마련
        self.cardsort = ['Clover','Diamond','Heart','Spade']
        self.cardnum = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        for s in self.cardsort:
            for n in self.cardnum:
                self.cards.append(s + n)

    def shuffle_cards(self):        #생성된 카드 한벌을 섞음
        random.shuffle(self.cards)
    
    def pop_card(self):             #덱에서 카드 한장을 꺼냄 (card_flow로 저장)
        card_flow.append(self.cards.pop(0))


class Person:                       #플레이어와 딜러의 상위class
    def __init__(self):             #Person의 인스턴스 생성시 개인 카드 보관함 생성 = pocket
        self.pocket =[]

    def dealt_card(self):           #card_flow에 임시보관된 카드를 한장 받음
        self.pocket.append(card_flow.pop(0))
    
    def value_assign(self):         #개인 카드 보관함에 있는 모든 카드의 점수를 배정(A값의 default는 11점)
        self.sum_t = 0
        for i in range(len(self.pocket)):
            if self.pocket[i][-1] in ['0', 'J', 'Q', 'K']:
                card_value = 10
            elif self.pocket[i][-1] in 'A':
                card_value = 11
            else:
                card_value = int(self.pocket[i][-1])
            self.sum_t = self.sum_t + card_value        #A값 선택 전 임시합
    
    def howmanya(self):            #개인 카드 보관함에 있는 A카드의 개수를 나타내고 카드 목록과 A의 개수를 알림
        self.quant_a = 0
        for i in range(len(self.pocket)):
            if self.pocket[i][-1] == 'A':
                exist_a = 1
            else:
                exist_a = 0
            self.quant_a = self.quant_a + exist_a
        print("\n당신의 카드목록입니다.>> ",self.pocket)
        print("\n당신은 A를 {}개 보유하고 있습니다.".format(self.quant_a))
    
    def trans_a(self):              #A 카드 중 1점으로 전환할 카드의 개수를 선택
        self.final_score = 0
        if self.quant_a == 0:
            self.final_score = self.sum_t #A 카드가 없다면 임시합이 현재 카드 목록의 최종합
        else:
            q = input("\n1점으로 간주할 A의 개수를 선택해주세요. {}개까지 가능합니다.(숫자로 입력) >> ".format(self.quant_a))
            while q not in ['0','1','2','3','4']:
                q = input("\n1점으로 간주할 A의 개수를 숫자로 입력해주세요. >>")
            while int(q) > self.quant_a:
                q = input("\n1점으로 간주할 A의 개수가 총 A의 개수를 초과합니다.\n0과 {}이내의 숫자로 선택해주세요. >>".format(self.quant_a))
            self.final_score = self.sum_t - 10 * int(q)

class Player(Person):       #Person의 하위클래스 : 카드추가여부를 입력값으로 결정하는 메쏘드를 추가
    def add_card(self):
        print("\n당신의 현재 점수는 {}점 입니다.\n".format(self.final_score))
        hos = input("카드를 더 받으시겠습니까?(y/n) >> ")
        self.det = 'hit'
        if hos == 'y':
            self.det = 'hit'
        else:
            self.det = 'stay'
        print("\n-----------------------------------------------------------")

class Dealer(Person):       #Person의 하위클래스
    def howmanya(self):     # 딜러 카드 보관함의 A개수를 파악하지만 카드 목록과 A의 개수를 표시하지는 않음
        self.quant_a = 0
        for i in range(len(self.pocket)):
            if self.pocket[i][-1] == 'A':
                exist_a = 1
            else:
                exist_a = 0
            self.quant_a = self.quant_a + exist_a   
    
    def trans_a(self):      #딜러 카드보관함에 포함된 A의 점수전환 여부를 입력값없이 결정
        self.final_score = 0
        if self.sum_t >= 17:
            while self.sum_t > 21 and self.quant_a >= 1:
                self.quant_a = self.quant_a - 1
                self.sum_t = self.sum_t - 10
            self.final_score = self.sum_t
        else :
            self.final_score = self.sum_t

    
    def add_card(self):     #딜러 카드추가여부를 입력값없이 결정
        self.det ='hit'
        if self.final_score < 17:
            self.det = 'hit'
        else:
            self.det = 'stay'

while True:
    start = input("게임을 시작하시려면 아무 키나 입력해주세요.")
    if start == '':
        pass

    deck = Deck()                   #deck 생성
    deck.shuffle_cards()            #deck 카드셔플
    dealer = Dealer()               #딜러 생성
    player = Player()               #플레이어 생성
    deck.pop_card()                 #덱에서 카드 1장 추출
    player.dealt_card()             #플레이어 카드 1장 수령
    deck.pop_card()                 #덱에서 카드 1장 추출
    dealer.dealt_card()             #딜러 카드 1장 수령

    while True:                     #딜러의 게임진행(stay조건이 충족되면 while loof를 빠져나옴)
        deck.pop_card()             #덱에서 카드 1장 추출
        dealer.dealt_card()         #딜러 카드 1장 수령
        dealer.value_assign()       #딜러 보유카드의 임시합을 계산
        dealer.howmanya()           #딜러 A카드 보유현황파악
        dealer.trans_a()            #딜러 A카드 점수전환
        dealer.add_card()           #딜러 카드추가여부 결정
        if dealer.det == 'stay':    
            break

    while True:
        deck.pop_card()             #덱에서 카드 1장 추출
        player.dealt_card()         #플레이어 카드 1장 수령
        player.value_assign()       #플레이어 보유카드의 임시합을 계산, 카드 목록과 임시합을 표시
        player.howmanya()           #플레이어 A카드 보유현황 파악 및 표시
        player.trans_a()            #플레이어 A카드 점수전환 선택 입력
        if player.final_score > 21: #게임중 플레이어 점수가 21점을 초과하면 강제종료
            break
        player.add_card()           #게임속행 가능상황에서 플레이어 카드추가여부 결정
        if player.det == 'stay':
            break

    print("Player ♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠")
    print("당신의 카드목록입니다.>> ",player.pocket)
    print("\n당신의 최종 점수는 {}점 입니다.".format(player.final_score))
    print("♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠\n")
    print("Dealer ♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤")
    print("딜러의 카드목록입니다.>> ",dealer.pocket)
    print("\n딜러의 최종 점수는 {}점 입니다.".format(dealer.final_score))
    print("♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤♤\n")

    if player.final_score > 21:                                                     #딜러의 점수에 관계없이 플레이어의 점수가 21점을 초과하면 패배
        print("21점을 초과하였습니다.\n\n당신은 패배하셨습니다.")
    elif player.final_score <= 21 and dealer.final_score > 21 :                     #플레이어의 점수가 21점 이하일때 딜러의 점수가 21점을 초과하면 승리
        print("딜러의 점수가 21점을 초과하였습니다.\n\n당신은 승리하셨습니다.")
    else:                                                                           #딜러와 플레이어의 점수가 모두 21점 이하일때 값을 비교
        if player.final_score > dealer.final_score:                                 #플레이어의 점수가 딜러의 점수보다 높으면 플레이어 승리
            print("당신의 점수가 딜러의 점수보다 높습니다.\n\n당신은 승리하셨습니다.")   
        elif player.final_score == dealer.final_score:                              #플레이어와 딜러의 점수가 같으면 무승부
            print("당신의 점수가 딜러의 점수와 같습니다.\n\n무승부입니다.") 
        else :                                                                      #플레이어의 점수가 딜러의 점수보다 낮으면 플레이어의 패배
            print("당신의 점수가 딜러의 점수보다 낮습니다.\n\n당신은 패배하셨습니다.")
    
    reset = input("\n게임을 더 하시겠습니까?(y/n)>> ")                                #재대결 여부 선택입력
    if reset == 'y':
        print("\n=======================================================")
        continue
    if reset == 'n':
        print("\n게임이 종료되었습니다.")
        break

import random,sys
HEARTS= chr(9829)
DIAMONDS= chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)
BACKSIDE = 'backside'
money = 1000000
A=0
def main():
    print('''21點紙牌遊戲

遊戲規則:
    1.21點的目標是使你的牌面點數比莊家更接近21點，但不超過21點。
    2.每張牌的點數計算如下：2-10點的牌面與它們上面所示的數字相同，J、Q、K的點數為10，A的點數為1或11。
    3.遊戲開始時，您會收到兩張牌，莊家也會收到兩張牌，但只有其中一張牌你可看到。
    4.莊家必須在自己的牌面總點數達到17或以上時停止要牌。
    5.如果您的點數比莊家高且不超過21點，您將贏得與您下注金額相等的賭注。
    6.如果您的點數比莊家低或超過21點，您將輸掉您的賭注。
    7.如果您的點數與莊家的點數相同，則平局，您的賭注將被退回。
    8.一開始發牌時拿到兩張牌若總和為21，稱為Blackjack，當局直接贏得1.5倍獎金。
    9.拿到五張牌且點數不超過21點稱為過五關，此時不需再與莊家比大小，直接贏得2倍獎金。
遊戲操作:
    遊戲一開始請先輸入玩家名稱以進行遊戲
    按(H)要求額外的牌，直到您認為您的點數足夠接近21點或您超過了21點。
    按(S)停牌，並與莊家比大小。
    按(D)則賭注加倍，並再獲得一張牌後直接比大小。
    若你覺得這局沒有勝算，可以按(C)投降，只是你會失去一半的籌碼。
註:
    本遊戲一開始的籌碼為1000000，每場賭注最多100000籌碼。
    遊戲進行到破產或按下(Q)鍵結束遊戲。
''')
    name=input("請問你叫什麼名稱?")
    if name=="":
        name="Player"
    money = 1000000
    while True:
        if money <= 0 :
            print("你破產了!")
            print('感謝遊玩本遊戲! '+'玩家 '+name+' 最終的籌碼是 '+str(int(money))+' 元')
            sys.exit()
        user_input = input('繼續進行遊戲？若要結束遊戲，請輸入"Q"鍵，否則按任意鍵繼續')
        if user_input == "Q":
            print('感謝遊玩本遊戲! '+'玩家 '+name+' 最終的籌碼是 '+str(int(money))+' 元')
            sys.exit()
        print(name,":",money,sep="")
        bet =min(getBet(money), 100000)
        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]
        print('賭注:', bet)
        while True:
            displayHands(playerHand, dealerHand, False)
            print()
            if getHandValue(playerHand) > 21:
                break
            if len(playerHand) == 5:
                break
            if len(playerHand) == 2 and getHandValue(playerHand) == 21:
                break
            move = getMove(playerHand, money - bet)
            if move == 'D':
                bet += bet
                print('賭金增加到{}.'.format(bet))
                print('賭金:', bet)
            if move in ('H','D'):
                newCard = deck.pop()
                rank, suit = newCard
                print('你抽到了{}{}.'.format(suit, rank))
                playerHand.append(newCard)
                if getHandValue(playerHand) > 21:
                    continue
            if move in ('S','D'):
                break
            if move == 'C':
                break
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)
                if getHandValue(playerHand) > 21:
                    break
        displayHands(playerHand, dealerHand, True)
        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)
        if len(playerHand) == 2 and playerValue == 21:
            if bet%2==1:
                bet=int(bet*1.5+0.5)
            else:
                bet=int(bet*1.5)
            print('Blackjack! 你贏得了1.5倍獎金共${}!'.format(bet))
            money += bet
        elif len(playerHand) == 5 and playerValue <= 21:
            print('恭喜過五關! 你贏得了2倍獎金共${}!'.format(2*bet))
            money += bet*2
        elif move == 'C' :
            if bet%2==1:
                bet=int(bet*0.5+0.5)
            else:
                bet=int(bet*0.5)
            print('投降輸一半! 你輸掉了0.5倍籌碼共${}!'.format(bet))
            money -=bet
        elif dealerValue > 21:
            print('莊家爆牌! 你贏得${}!'.format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('你輸掉了${}!'.format(bet))
            money -= bet
        elif playerValue > dealerValue :
            print('你贏得${}!'.format(bet))
            money += bet
        elif playerValue == dealerValue:
            print('本局平手')
def getBet(maxBet):
    while True:
        print('請問你要賭多少錢?(1~{})'.format(min((maxBet),100000)))
        bet = input('> ').upper().strip()      
        if not bet.isdecimal():
            print("請重新輸入！")
            continue
        bet=int(bet)
        if 1 <= bet <= maxBet:
            return bet
def getDeck():
    deck = []
    for suit in (HEARTS,DIAMONDS,SPADES,CLUBS):
        for rank in range(2,11):
            deck.append((str(rank),suit))
        for rank in ('J','Q','K','A'):
            deck.append((rank,suit))
    random.shuffle(deck)
    return deck
def displayHands(playerHand, dealerHand, showDealerHand):
    print()
    if showDealerHand:
        print('莊家:', getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print('莊家:???')
        displayCards([BACKSIDE] + dealerHand[1:])
    print('玩家:', getHandValue(playerHand))
    displayCards(playerHand)
def getHandValue(cards):
    value = 0
    number0fAces = 0
    for card in cards:
        rank = card[0]
        if rank == 'A':
            number0fAces += 1
        elif rank in ('K','Q','J'):
            value += 10
        else:
            value += int(rank)
    value += number0fAces
    for i in range(number0fAces):
        if value + 10 <= 21:
            value += 10
    return value
def displayCards(cards):
    rows = [' ',' ',' ',' ',' ']
    for i, card in enumerate(cards):
        rows[0] += '___  '
        if card == BACKSIDE:
            rows[1] += '|###| '
            rows[2] += '|###| '
            rows[3] += '|###| '
        else:
            rank, suit = card
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))
    for row in rows:
        print(row)
def getMove(playerHand, money):
    while True:
        moves = ['輸入"H"加牌', '輸入"S"停牌']
        if len(playerHand) == 2 and money > 100000:
            moves.append('輸入"D"賭金加倍')
        if len(playerHand) == 2:
            moves.append('輸入"C"投降')
        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H','S'):
            return move
        elif move == 'D' and '輸入"D"賭金加倍' in moves:
            return move
        elif move == 'C' and '輸入"C"投降' in moves:
            return move
        else:print("請重新輸入！")
if __name__ == '__main__':
    main()

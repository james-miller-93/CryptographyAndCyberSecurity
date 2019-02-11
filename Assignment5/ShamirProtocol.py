import ShamirParty

parties = []

for i in range(4):
    parties.append(ShamirParty.Party(i+1))

message = 3

dealer = ShamirParty.Party(0)

dealer.Share(message,parties)

for i in range(4):
    parties[i].SendShare(parties)

for i in range(4):
    parties[i].Reconstruct()

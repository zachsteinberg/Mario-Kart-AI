checkpoint = 0

function reward() 
    lap = data.Lap - 127
    pos = data.POS --This varies between 0 and 40 or so, depending on track. For Mario Circuit, goes from 0 to 29.
    speed = data.OverallSpeed -- this varies between 0 and 1000

	
	-- Annoyingly, you start at the highest position. To counter this, I reset to -1
	if pos == 29 then
		pos = -1
	end
		
	-- I make sequential checkpoints so the agent gets rewarded for getting further into the map
	-- They are gated so you can only get a checkpoint if you've gotten the previous one, this stops the agent from going backwards

	if pos > 20 and checkpoint == 3 then
		checkpoint = 4	
	elseif pos > 15 and pos < 20 and checkpoint == 2 then
		checkpoint = 3	
	elseif pos > 10 and pos < 15 and checkpoint == 1 then
		checkpoint = 2	
	elseif pos > 5 and pos < 10 and checkpoint == 0 then
		checkpoint = 1	
	elseif pos < 5 then
		checkpoint = 0
	end
		
    return (checkpoint * 25) + (lap * 1000) + (speed / 100)
end
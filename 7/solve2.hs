step :: (Int, Int, [Int]) -> String -> [Int] -> (Int, [Int])
step (_, accum, state) "" _ = (accum, state)
step (prev, prevAccum, state) (s : ss) (x : xs) = step (next, accum, f (s, x) state) ss xs
  where
    f (a, b) state
      | a == '.' = state ++ [b + prev]
      | a == '^' && b /= 0 = init state ++ [last state + b, 0]
      | a == '^' && b == 0 = state ++ [0]
      | a == 'S' = state ++ [1]
    next = if s == '^' then x else 0
    accum = if s == '^' then prevAccum + x else prevAccum

loopOver :: Int -> [Int] -> [String] -> Int
loopOver accum _ [] = accum
loopOver accum state (x : xs) =
  let (a, b) = step (0, 0, []) x state
   in loopOver (a + accum) b xs

main :: IO () = do
  io <- getContents
  print $ 1 + loopOver 0 (replicate (length . head $ lines io) 0) (lines io)

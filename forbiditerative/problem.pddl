(define (problem pb7)
(:domain blocks)
(:objects D J H P B Q G E I M C F A O N L K - block)
(:INIT (CLEAR K) (CLEAR L) (CLEAR N) (ONTABLE O) (ONTABLE A) (ONTABLE F)
 (ON K C) (ON C M) (ON M I) (ON I E) (ON E G) (ON G Q) (ON Q B) (ON B P)
 (ON P H) (ON H J) (ON J O) (ON L D) (ON D A) (ON N F) (HANDEMPTY))
(:goal (and
(ON P Q)
 (ON Q L)
 (ON L N)
 (ON N C)
 (ON C I)
 (ON I K)
 (ON K F)
 (ON F J)
 (ON J B)
 (ON B G)
 (ON G A)
 (ON A H)
 (ON H E)
 (ON E O)
 (ON O M)
 (ON M D)
))
)
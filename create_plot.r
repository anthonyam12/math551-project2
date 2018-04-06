run <- function() {
    game <- games[games$game_number == 0, ]
    plot(game$humans, xlim=range(1:9), ylim=range(0:51), type='l', col='orange', 
         ylab='population size', xlab='timestep (turn)', main='Change in Populations for 10,000 Simulated Games')
    lines(game$zombies, col='green')
    lines(game$removed, col='red')
    
    for(i in c(1:9999)) {
        game <- games[games$game_number == i, ]
        lines(game$humans, col='orange')
        lines(game$zombies, col='green')
        lines(game$removed, col='red')
    }
    legend(6.75, 32, c("humans", "zombies", "removed"), col=c("orange", "green", "red"), cex=0.75, lty=1)
}
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace DBAForge.Worker;

public sealed class Worker(ILogger<Worker> logger) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        logger.LogInformation("DBAForge worker started.");

        await Task.Delay(Timeout.InfiniteTimeSpan, stoppingToken);
    }
}

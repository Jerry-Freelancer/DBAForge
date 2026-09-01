using DBAForge.Contracts;

namespace DBAForge.UnitTests;

public sealed class HealthResponseTests
{
    [Fact]
    public void CreatesHealthyStatusResponse()
    {
        var response = new HealthResponse("Healthy");

        Assert.Equal("Healthy", response.Status);
    }
}

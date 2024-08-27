import locust


class ArpavPpcvUser(locust.FastHttpUser):
    wait_time = locust.between(1, 5)

    @locust.task
    def coverage_configurations(self):
        self.client.get("/api/v2/coverages/coverage-configurations")

    @locust.task
    def configuration_parameters(self):
        self.client.get("/api/v2/coverages/configuration-parameters")

    @locust.task
    def coverage_identifiers(self):
        self.client.get("/api/v2/coverages/coverage-identifiers")

    @locust.task
    def stations(self):
        self.client.get("/api/v2/observations/stations")

    @locust.task
    def variables(self):
        self.client.get("/api/v2/observations/variables")

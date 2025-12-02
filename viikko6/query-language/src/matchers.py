class And:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        for matcher in self._matchers:
            if not matcher.test(player):
                return False

        return True


class PlaysIn:
    def __init__(self, team):
        self._team = team

    def test(self, player):
        return player.team == self._team


class HasAtLeast:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)

        return player_value >= self._value


class All:
    def test(self, player):
        return True


class Not:
    def __init__(self, matcher):
        self.matcher = matcher

    def test(self, player):
        return not self.matcher.test(player)


class HasFewerThan:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)

        return player_value < self._value


class Or:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        for matcher in self._matchers:
            if matcher.test(player):
                return True

        return False


class QueryBuilder:
    def __init__(self, matchers=None):
        if matchers is None:
            self._matchers = []
        else:
            self._matchers = matchers[:]

    def plays_in(self, team):
        new_matchers = self._matchers[:]
        new_matchers.append(PlaysIn(team))
        return QueryBuilder(new_matchers)

    def has_at_least(self, value, attr):
        new_matchers = self._matchers[:]
        new_matchers.append(HasAtLeast(value, attr))
        return QueryBuilder(new_matchers)

    def has_fewer_than(self, value, attr):
        new_matchers = self._matchers[:]
        new_matchers.append(HasFewerThan(value, attr))
        return QueryBuilder(new_matchers)

    def one_of(self, *queries):
        matchers = [query.build() for query in queries]
        new_matchers = self._matchers[:]
        new_matchers.append(Or(*matchers))
        return QueryBuilder(new_matchers)

    def build(self):
        if len(self._matchers) == 0:
            return All()

        if len(self._matchers) == 1:
            return self._matchers[0]

        return And(*self._matchers)

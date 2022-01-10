'''Houses the main class for canister.py.'''
# canister.py

# imports
import urllib
from .errors import InitializationError
from .requests import canister_request, piracy_repos
from .types import Repo, Package
from typing import List

class Canister():
    '''The main Canister class.
    Args:
        user_agent (str): User Agent to pass to the Canister API.
    '''
    def __init__(self, user_agent: str):
        if user_agent is None:
            raise InitializationError('You did not specify a User Agent to use.')
        self.ua = user_agent

    async def search_package(self, query: str, search_fields: str = "name,author,maintainer,description", limit: int = 100) -> List[Package]:
        '''Search for a package.
        Args:
            query (str): Query to search for.
            search_fields (Optional[str]): Fields to search for. (defaults to 'name,author,maintainer,description')
            limit (Optional[str]): Response length limit. (defaults to 100)
        Returns:
            List[Package]: List of packages that Canister found matching the query.
        '''
        # normalize query string
        query = urllib.parse.quote(query)
        # make request
        response = await canister_request(f'/packages/search?query={query}&limit={limit}&searchFields={search_fields}&responseFields=name,author,maintainer,description&responseFields=identifier,header,tintColor,name,price,description,packageIcon,repository.uri,repository.name,author,maintainer,latestVersion,nativeDepiction,depiction', self.ua, 1)
        # convert packages to Package objects
        return [Package(package) for package in response.get('data')]
    
    async def search_repo(self, query: str) -> List[Repo]:
        '''Search for a repo.
        Args:
            query (str): Query to search for.
        Returns:
            List[Repo]: List of repos that Canister found matching the query.
        '''
        # normalize query string
        query = urllib.parse.quote(query)
        # make request
        response = await canister_request(f'/repositories/search?query={query}', self.ua, 1)
        # convert packages to Repository objects
        return [Repo(repo) for repo in response.get('data')]

    async def is_repo_piracy(self, query: str) -> bool:
        '''Find out if a repo is piracy.
        Args:
            query (str): Repo URI.
        Returns:
            bool: Whether or not the repo is piracy.
        '''
        # trim url string
        query = query.replace('https://', '').replace('http://', '')
        # get piracy repos
        r = await piracy_repos()
        # return
        return query in r
import {
  Button,
  Radio,
  RadioGroup,
  RangeSlider,
  RangeSliderFilledTrack,
  RangeSliderThumb,
  RangeSliderTrack,
  Stack,
} from '@chakra-ui/react';

import { useCallback, useEffect, useState } from 'react';
import { HiSearchCircle } from 'react-icons/all';

import { SERVER_URL } from '../utils/constants';
import {
  Filter,
  FilterTitle,
  FilterValues,
  ListButton,
  ListButtonLink,
  ListButtonsContainer,
  ListContent,
  ListItemsContainer,
  ListMenu,
  ListSearchButton,
  ListSearchContainer,
  ListSearchInput,
  ListStyledContainer,
} from './styles';

export function List({
  location: {
    state: { search: initialSearch },
  },
}) {
  const [search, setSearch] = useState(initialSearch);
  const [area, setArea] = useState(-1);
  const [salary, setSalary] = useState([0, 500000]);

  const [areaData, setAreaData] = useState([]);
  const [moreAreas, setMoreAreas] = useState(false);

  useEffect(() => {
    fetch(`${SERVER_URL}/api/area/list?offset=0&limit=100`)
      .then((res) => res.json())
      .then((data) => {
        setAreaData(data);
      });
  }, []);

  const handleFilter = useCallback(() => {
    const payloadSearch = search || '*';
    const payloadArea = area === -1 ? '' : `&areas=${area}`;

    fetch(
      `${SERVER_URL}/api/vacancy/filter/?search_arg=${payloadSearch}${payloadArea}&currency=RUR&sf=${salary[0]}&st=${salary[1]}&offset=0&limit=100`
    )
      .then((res) => res.json())
      .then((data) => console.log(data));
  }, [area, search, salary]);

  useEffect(() => {
    handleFilter();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <ListStyledContainer>
      <ListMenu>
        <ListButtonLink to="/">На главную</ListButtonLink>

        <Filter>
          <FilterTitle>Регион</FilterTitle>

          <RadioGroup onChange={(value) => setArea(Number(value))} value={area}>
            <Stack>
              {areaData
                .slice(0, moreAreas ? areaData.length - 1 : 3)
                .map(({ id, name }) => (
                  <Radio
                    key={id}
                    colorScheme="green"
                    name={id}
                    size="md"
                    value={id}>
                    {name}
                  </Radio>
                ))}
            </Stack>
          </RadioGroup>
          {!moreAreas && (
            <Button
              colorScheme="blue"
              onClick={() => setMoreAreas(true)}
              variant="link">
              показать все
            </Button>
          )}
        </Filter>

        <FilterTitle>Уровень дохода</FilterTitle>
        <RangeSlider onChange={setSalary} value={salary}>
          <RangeSliderTrack>
            <RangeSliderFilledTrack />
          </RangeSliderTrack>
          <RangeSliderThumb index={0} />
          <RangeSliderThumb index={1} />
        </RangeSlider>

        <FilterValues>
          <span>{salary[0]}</span>
          <span>{salary[1]}</span>
        </FilterValues>
      </ListMenu>

      <ListContent>
        <ListSearchContainer>
          <ListSearchInput
            onChange={({ target: { value } }) => setSearch(value)}
            onKeyDown={({ key }) => key === 'Enter' && handleFilter()}
            placeholder="Профессия, должность или вакансия"
            value={search}
          />

          <ListSearchButton onClick={handleFilter}>
            <HiSearchCircle size={35} />
          </ListSearchButton>
        </ListSearchContainer>

        <ListButtonsContainer>
          <ListButton>Построить диаграмму</ListButton>
          <ListButton>Построить граф</ListButton>
          <ListButton>Разместить вакансию</ListButton>
        </ListButtonsContainer>

        <ListItemsContainer>Нет данных</ListItemsContainer>
      </ListContent>
    </ListStyledContainer>
  );
}
